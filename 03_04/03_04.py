import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Helper function to print search results
def print_output(docs):
    for doc in docs:
        print('The output is: {}. \n\nThe metadata is {} \n\n'.format(doc.page_content, doc.metadata))
# Load API key and vector database
db = FAISS.load_local(
    "../faiss_index", 
    OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small"), 
    allow_dangerous_deserialization=True
)
# Perform similarity search
query = "What are the medicinal insights from the Voynich manuscript?"
print(f"--- Searching for: '{query}' ---")
docs = db.similarity_search(query)

print(f"Number of search results: {len(docs)}")
print_output(docs)
