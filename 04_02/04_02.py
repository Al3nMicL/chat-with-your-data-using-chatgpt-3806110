import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

from langchain_openai import ChatOpenAI

# initialize the LLM we'll use - OpenAI GPT 4.1 Nano
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4.1-nano-2025-04-14")

print("--- Calling LLM without RAG: 'What are the medicinal insights from the Voynich manuscript?' ---")
# prompt the model with no additional knowledge of the Voynich manuscript beyond pretraining 
print(llm.invoke("What are the medicinal insights from the Voynich manuscript?"))

print("\n--- Calling LLM without RAG: 'What is Aetherfloris Ventus?' ---")
print(llm.invoke("What is Aetherfloris Ventus?"))

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# load vector database from disk
db = FAISS.load_local("../faiss_index", 
                      OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small"), 
                      allow_dangerous_deserialization=True)

# config retriever - use the similarity search capabilities of a vector store to facilitate retrieval
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 6})

from langchain_classic import hub

# implement a chain - put together multiple calls in a logical sequence
prompt_rag = hub.pull("rlm/rag-prompt")
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# combine multiple steps in a single chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_rag
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

# preserve conversation history
from langchain_classic.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

system_prompt = """Given the chat history and a recent user question \
generate a new standalone question \
that can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed or otherwise return it as is."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

retriever_with_history = create_history_aware_retriever(
    llm, retriever, prompt
)

print("\n--- Retriever with History setup successfully ---")
print("Prompt Input Variables:", prompt.input_variables)
print("Prompt Input Types:", prompt.input_types)
