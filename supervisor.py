# %%
from langchain.chat_models import init_chat_model
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv


load_dotenv()
# %%
class State(TypedDict):
    messages: list[BaseMessage]
    image: str | None
    next: str
# %%
llm = init_chat_model("google_genai:gemini-3.1-flash-lite")
# %%
def supervisor(state: State) -> State:
    next_agent = llm.invoke([
        SystemMessage(content="""
                        You are a routing assistant.

                        Available agents:
                        - quotation_agent: Generates quotation for a service, using the dimensions provided, either by text or image
                        - stock_agent: Checks the stock of a particular product
                        - image_agent: Fetches and returns the image of a particular service requested by the user
                        - rag_agent: Answers general queries related to the company.


                        Return ONLY the name of the most suitable agent.
                        Return rag_agent if you don't think query is not suitable for the other 3."""),
        *state["messages"]
    ])
    state["next"] = next_agent.text
    return state
# %%
from agents.check_stock_agent import stock_agent
from agents.generate_quotation_agent import quotation_agent
from agents.get_image_agent import image_agent
from agents.rag_agent import rag_agent
# %%
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)

builder.add_node("supervisor", supervisor)
builder.add_node("stock_agent", stock_agent)
builder.add_node("quotation_agent", quotation_agent)
builder.add_node("image_agent", image_agent)
builder.add_node("rag_agent", rag_agent)
# %%
builder.add_edge(START, "supervisor")

builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next"],
    {
        "stock_agent": "stock_agent",
        "quotation_agent": "quotation_agent",
        "rag_agent": "rag_agent",
        "image_agent": "image_agent"
    },
)

builder.add_edge("stock_agent", END)
builder.add_edge("quotation_agent", END)
builder.add_edge("image_agent", END)
builder.add_edge("rag_agent", END)

graph = builder.compile()

if __name__ == "__main__":
    response = graph.invoke({"messages": "give me image of oak flooring", "next": ""})
    print(response["messages"][-1].content)