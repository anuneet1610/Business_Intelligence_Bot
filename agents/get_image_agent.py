# %%
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()
# %%
from tools.get_image import get_product_image

# %%
llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it")
# %%
system_prompt = (
    "You are a helpful image extraction assistant. The user may ask for image of a particular product."
    "You need to extract the name of the product for which the user is asking image for."
    "Using this product name, call get_product_image tool to get the URL of the product image."
    "Return a JSON in the following format, separating the URL as well as your reply message:"
    "{\"message\": "
    "\"image_url\":  "
)

image_agent = create_agent(
    llm,
    tools=[get_product_image],
    system_prompt=system_prompt,
)
# %%
def ask(question: str) -> None:
    result = image_agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)
# %%
if __name__ == "__main__":
    ask("Give me the image of oak flooring")

