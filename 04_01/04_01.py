import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
# helper functions
def print_output(docs):
    for doc in docs:
        print('The output is: {}. \n\nThe metadata is {} \n\n'.format(doc.page_content, doc.metadata))

from langchain_openai import ChatOpenAI

# initialize the LLM we'll use - OpenAI GPT 3.5 Turbo
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-0125")
#prompt the model with no additional knowledge of the Voynich manuscript beyond pretraining 
print("--- Calling LLM without RAG: 'What are the medicinal insights from the Voynich manuscript?' ---")
response1 = llm.invoke("What are the medicinal insights from the Voynich manuscript?")  
print(response1)

print("\n--- Calling LLM without RAG: 'What is Aetherfloris Ventus?' ---")
response2 = llm.invoke("What is Aetherfloris Ventus?")
print(response2)

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# load vector database from disk
db = FAISS.load_local("../faiss_index", 
                      OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small"), 
                      allow_dangerous_deserialization=True)
# config retriever - use the similarity search capabilities of a vector stror to facilitate retrieval
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 6})

from langchain_classic import hub

prompt = hub.pull("rlm/rag-prompt")
# implement a chain - put together multiple calls in a logical sequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# combine multiple steps in a single chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser() #convert the chat message to a string
)
# send LLM's response to the user
print("\n--- Calling LLM with RAG: 'What are the medicinal insights from the Voynich manuscript?' ---")
for chunk in rag_chain.stream("What are the medicinal insights from the Voynich manuscript?"):
    print(chunk, end="", flush=True)
print() # (for formatting) add a newline after each stream

print("\n--- Calling LLM with RAG: 'What is Aetherfloris Ventus?' ---")
for chunk in rag_chain.stream("What is Aetherfloris Ventus?"):
    print(chunk, end="", flush=True)
print() 

print("\n--- Calling LLM with RAG: 'What's the most important part of the Voynich manuscript?' ---")
for chunk in rag_chain.stream("What's the most important part of the Voynich manuscript?"):
    print(chunk, end="", flush=True)
print() 
