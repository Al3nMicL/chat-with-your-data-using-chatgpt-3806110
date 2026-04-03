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
print("--- Searching for: 'What is Aetherfloris Ventus' ---")
docs1 = db.similarity_search("What is Aetherfloris Ventus")
print(f"Number of search results: {len(docs1)}")
print_output(docs1)

print("--- Searching for: 'Can you recommend a herbal brew?' ---")
docs2 = db.similarity_search("Can you recommend a herbal brew?")
print(f"Number of search results: {len(docs2)}")
print_output(docs2)

print("--- Searching for: 'What is the orbit of the sun-like figure?' ---")
docs3 = db.similarity_search("What is the orbit of the sun-like figure?")
print(f"Number of search results: {len(docs3)}")
print_output(docs3)
