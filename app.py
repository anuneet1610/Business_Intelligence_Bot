from fastapi import FastAPI
from pydantic import BaseModel
from supervisor import graph
from langchain_core.messages import HumanMessage

app = FastAPI()

class Query(BaseModel):
    message: str
    image: str | None = None      # base64 string

@app.post("/chat")
def chat(query: Query):
    if query.image:
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": query.message,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{query.image}"
                    },
                },
            ]
        )
    else:
        message = HumanMessage(content=query.message)

    result = graph.invoke({
        "messages": [message],
        "image": query.image,
        "next": ""
    })
    last_message = result["messages"][-1]

    response = getattr(last_message, "content", None) or getattr(last_message, "text", "")

    return {"response": response}