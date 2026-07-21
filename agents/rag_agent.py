# %%
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import base64
from dotenv import load_dotenv

load_dotenv()
# %%
from tools.retrieve_docs import retrieve_docs
# %%
llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it")
# %%
system_prompt = (
    "You are a helpful answer generating assistant. You are given a tool retrieve_docs to get context for answering the user query."
    "You need to answer the user query only using the context given by the retrieve_docs tool."
)
# %%
rag_agent = create_agent(
    llm,
    tools=[retrieve_docs],
    system_prompt=system_prompt,
)
# %%
def ask(question):
    result = rag_agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].text)
# %%
if __name__ == "__main__":
    ask("Is Blinkit part of Zomato?")