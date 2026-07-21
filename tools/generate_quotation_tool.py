import os
from langchain.tools import tool
import requests
import uuid

API_KEY = os.getenv("HTML2PDF_API_KEY")

@tool
def generate_quotation_pdf(data: dict) -> str:
    """
    Generate a quotation PDF from quotation data.

    Args:
        data: {
            "items": [
                {
                    "product": "...",
                    "length": ...,
                    "width": ...,
                    "price": ...,
                    "total": ...
                }
            ],
            "grandTotal": ...
        }

    Call this once per quotation request, with all services included as separate entries in items.

    Returns:
        HTML code to generate the PDF file
    """

    rows = ""

    for item in data["items"]:
        rows += f"""
        <tr>
            <td>{item["product"]}</td>
            <td>{item["length"]}</td>
            <td>{item["width"]}</td>
            <td>₹{item["price"]}</td>
            <td>₹{item["total"]}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial;
                padding:20px;
            }}

            table {{
                width:100%;
                border-collapse:collapse;
            }}

            th,td {{
                border:1px solid #ccc;
                padding:10px;
                text-align:center;
            }}

            th {{
                background:#f5f5f5;
            }}

            .total {{
                margin-top:20px;
                text-align:right;
                font-weight:bold;
                font-size:18px;
            }}
        </style>
    </head>

    <body>

    <h1 style="text-align:center;">Quotation</h1>

    <table>

        <thead>
            <tr>
                <th>Service</th>
                <th>Length (m)</th>
                <th>Width (m)</th>
                <th>Price</th>
                <th>Total</th>
            </tr>
        </thead>

        <tbody>
            {rows}
        </tbody>

    </table>

    <div class="total">
        Grand Total: ₹{data["grandTotal"]}
    </div>

    </body>
    </html>
    """

    return html

    # response = requests.post(
    #     "https://api.html2pdf.app/v1/generate",
    #     json={
    #         "apiKey": API_KEY,
    #         "html": html,
    #     },
    #     timeout=60,
    # )
    #
    # response.raise_for_status()
    #
    # # Response is raw PDF bytes, not JSON
    # content_type = response.headers.get("Content-Type", "")
    # if "application/pdf" not in content_type and not response.content.startswith(b"%PDF"):
    #     # fallback in case it *does* return JSON in some cases
    #     return response.json()["url"]
    #
    # filename = f"quotation_{uuid.uuid4().hex}.pdf"
    # filepath = os.path.join("generated_pdfs", filename)  # make sure this dir exists
    # os.makedirs("generated_pdfs", exist_ok=True)
    #
    # with open(filepath, "wb") as f:
    #     f.write(response.content)
    #
    # return filepath  # or a URL if you're serving this directory over HTTP