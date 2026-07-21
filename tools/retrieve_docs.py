from langchain_community.vectorstores import SupabaseVectorStore
import os
from dotenv import load_dotenv
from supabase import create_client
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools import tool

load_dotenv()

# Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents"
)

retriever = vector_store.as_retriever()

@tool
def retrieve_docs(query: str):
    '''Taking input as the user query, it performs a sematic search in the database to return the top 2 most similar chunks.'''
    docs = vector_store.similarity_search(
        query,
        k=2
    )
    return docs