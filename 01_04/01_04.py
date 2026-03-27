from langchain_community.document_loaders import PyPDFLoader

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

from langchain_text_splitters import CharacterTextSplitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
)

docs = text_splitter.split_documents(pages)

print(f"Total documents after splitting: {len(docs)}\n")

print("--- docs[3] ---")
print(docs[3], "\n")

print("--- docs[41] ---")
print(docs[41], "\n")

print("--- docs[20] ---")
print(docs[20], "\n")
