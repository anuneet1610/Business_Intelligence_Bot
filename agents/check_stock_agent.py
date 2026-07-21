# %%
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
# %%
from dotenv import load_dotenv

load_dotenv()
# %%
# 1. Define configuration constants
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "credentials.json"

# Extract this ID from your Google Sheet URL:
# https://google.com[SPREADSHEET_ID_HERE]/edit
SPREADSHEET_ID = "1kacixGz_mvfAYpPLlq6ngYsreaWbZl_ZHJekLtvmgJk"
RANGE_NAME = "Sheet1!A1:E10"  # Adjust the sheet name and cell range
# %%
@tool
def get_sheets_data(product: str) -> int:
    """Fetches stock data from Google Sheets, and returns the quantity for the particular product."""
    try:
        # 2. Authenticate using the service account JSON key file
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        # 3. Build the Sheets API service client
        service = build("sheets", "v4", credentials=creds)

        # 4. Call the Sheets API to fetch cell values
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
            .execute()
        )

        # 5. Extract values from the API payload
        rows = result.get("values", [])

        if not rows:
            print("No data found in the specified range.")
            return None

        for i in range(1,len(rows)):
            if rows[i][0].lower() == product.lower():
                return int(rows[i][1])
        return -1

    except HttpError as error:
        print(f"An API error occurred: {error}")
        return None
    except FileNotFoundError:
        print(f"Error: The file '{SERVICE_ACCOUNT_FILE}' was not found.")
        return None
# %%
llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it")
# %%
stock_agent = create_agent(
    llm,
    tools=[get_sheets_data],
    system_prompt="You are a helpful assistant, who receives the query of the user, understands it, and answers with the product quantity.",
)
# %%
def ask(question: str):
    result = stock_agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)
# %%
if __name__ == "__main__":
    ask("What is the stock of Shampoo?")