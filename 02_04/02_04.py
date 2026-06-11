import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load PDF
loaders = [
    PyPDFLoader("../Data/botanical.pdf"),
    PyPDFLoader("../Data/astronomical.pdf"),
    PyPDFLoader("../Data/biological.pdf"),
    PyPDFLoader("../Data/cosmological.pdf"),
    PyPDFLoader("../Data/culinary.pdf"),
    PyPDFLoader("../Data/pharmaceutical.pdf")
]

pages = []

for loader in loaders:
    pages.extend(loader.load())
# split PDF into chunks
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
)

docs = text_splitter.split_documents(pages)
print(f"Total documents split: {len(docs)}")
# convert documents to embeddings and load into vector database
embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")

vectordb = FAISS.from_documents(docs, embeddings_model)
print(f"Total documents added to vector database: {vectordb.index.ntotal}")
# Persist Vector Store
vectordb.save_local("../faiss_index")
print("Vector database persisted to '../faiss_index'")
