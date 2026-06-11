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

docs = []

for loader in loaders:
    docs.extend(loader.load())

print(f"Length of docs[0].page_content: {len(docs[0].page_content)}\n")

print("--- docs[0].page_content[:500] ---")
print(docs[0].page_content[:500], "\n")

print("--- docs[5].page_content[:700] ---")
print(docs[5].page_content[:700], "\n")

print(f"Total documents loaded: {len(docs)}\n")

print("--- docs[0] ---")
print(docs[0], "\n")

print("--- docs[1] ---")
print(docs[1], "\n")

print("--- docs[23] ---")
print(docs[23], "\n")
