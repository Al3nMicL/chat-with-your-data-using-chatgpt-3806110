import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import OpenAIEmbeddings

_ = load_dotenv(find_dotenv()) # read local .env file
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")

embeddings = embeddings_model.embed_documents(
    [
        "I love learning!",
        "Learning is fun!",
        "Never stop learning!",
        "Explore LinkedIn Learning courses.",
        "Watch my other courses"
    ]
)

print(f"Number of embeddings generated: {len(embeddings)}")

# Printing first 5 values to keep CLI output manageable
print("\n--- embeddings[0][:5] ---")
print(embeddings[0][:5])

print("\n--- embeddings[1][:5] ---")
print(embeddings[1][:5])

embedded_query = embeddings_model.embed_query("What is the best way to learn new things?")

print("\n--- embedded_query[:5] ---")
print(embedded_query[:5])
