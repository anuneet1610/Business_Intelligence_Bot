from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain.tools import tool

# 1. Define configuration constants
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "credentials.json"

# Extract this ID from your Google Sheet URL:
# https://google.com[SPREADSHEET_ID_HERE]/edit
SPREADSHEET_ID = "1W8EF-lcWBQlxpbKH9bnjNCWvkovE6h_OJG7Hpp_qtyc"
RANGE_NAME = "Sheet1"  # Adjust the sheet name and cell range

@tool
def get_price_data(service_name: str) -> list:
    '''Fetches cost of the service for 1 square meter area, from Google Sheets. Remember to send just the service name as parameter. For example, if service is "flooring", just send "flooring" instead of "flooring service".'''
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
            if rows[i][0] == service_name:
                return int(rows[i][1])
        return -1

    except HttpError as error:
        print(f"An API error occurred: {error}")
        return None
    except FileNotFoundError:
        print(f"Error: The file '{SERVICE_ACCOUNT_FILE}' was not found.")
        return None