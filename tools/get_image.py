from langchain.tools import tool
import os
from supabase import create_client
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

supabase = create_client(url, key)

@tool
def get_product_image(product_name: str):
    """Using the name of the product, returns the url of the image from supabase"""

    result = (
        supabase.table("images")
        .select("file_path")
        .ilike("product", f"%{product_name}%")
        .execute()
    )

    if not result.data:
        return "No image found."

    path = result.data[0]["file_path"]
    print(path)
    return supabase.storage.from_("images").get_public_url(path)
