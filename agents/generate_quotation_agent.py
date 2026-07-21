from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import json

load_dotenv()

from tools.generate_quotation_tool import generate_quotation_pdf
from tools.get_price_data import get_price_data
from tools.convert_cm_to_m import convert_cm_to_m
from tools.calculate_total_cost import calculate_total_cost
from tools.calculate_grand_total import calculate_grand_total

llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it")

system_prompt=(
    "You are a helpful quotation generation assistant. The user may ask for a quotation "
    "for one or more services. For each service mentioned, extract its name. If the user provided an image, extract the length "
    "and width of the area from it. If no image is provided, extract the dimensions from the user's text. Fetch the corresponding per-square-meter price, and calculate its total cost. "
    "Once you have gathered all services, combine them into a SINGLE call to "
    "generate_quotation_pdf with one entry per service in `items`, and grandTotal set to "
    "the sum of all item totals. Do not call generate_quotation_pdf more than once per request."
    "Return a pure JSON in the following format, with message containing your message, and html containing the HTML code given by generate_quotation_pdf.:"
    "{\"message\": "
    "\"html\": }"
    "No markdown, No '''json, No code fences, just pure JSON"
)

quotation_agent = create_agent(
    llm,
    tools=[get_price_data, convert_cm_to_m, calculate_total_cost, generate_quotation_pdf, calculate_grand_total],
    system_prompt=system_prompt,
)



def ask(message: str, image_base64: str | None = None):

    if image_base64:
        user_message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": message,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    },
                },
            ]
        )
    else:
        user_message = HumanMessage(content=message)

    result = quotation_agent.invoke({
        "messages": [user_message]
    })

    content = result["messages"][-1].content
    parsed = json.loads(content)

    return parsed

# %%
# if __name__ == "__main__":
#     query_message_img = HumanMessage(
#         content=[
#             {"type": "text",
#              "text": "Generate a quotation for flooring service for an area with dimensions given in the image"},
#             {
#                 "type": "image_url",
#                 "image_url": {
#                     "url": f"data:image/png;base64,{base64_image}"
#                 },
#             },
#         ]
#     )
#     # %%
#     query_message_txt = "Generate a quotation for flooring service for an area with dimensions of 5 meters x 5 meters"
#     ask()
#
# with open("images (1).png", "rb") as f:
#     image = base64.b64encode(f.read()).decode()
#
# answer = ask(
#     "Generate quotation for flooring service",
#     image
# )
#
# print(answer)
