import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

from langchain_community.document_loaders import PyPDFLoader

# Load documents
loader = PyPDFLoader('michelle_obama_speech.pdf')
pages = loader.load()

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Load the document, split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(pages)

from langchain_community.vectorstores import FAISS

embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")

# Load it into the vector store and embed
vectordb = FAISS.from_documents(documents, embeddings_model)

print(f"Total documents in vector store: {vectordb.index.ntotal}")

# Persist Data in your Vector Store
vectordb.save_local("faiss2_index")
print("Vector store saved to 'faiss2_index'")

# Load Vector Store
new_db = FAISS.load_local("faiss2_index", embeddings_model, allow_dangerous_deserialization=True)
print(f"Loaded vector store from 'faiss2_index', total documents: {new_db.index.ntotal}")
