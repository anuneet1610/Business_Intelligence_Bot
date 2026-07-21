# %%
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
# %%
from dotenv import load_dotenv

load_dotenv()

from tools.get_sheets_data import get_sheets_data
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
