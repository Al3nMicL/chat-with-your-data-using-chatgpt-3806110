import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# load vector database from disk
db = FAISS.load_local("../faiss_index", 
                      OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small"), 
                      allow_dangerous_deserialization=True)

# config retriever - use the similarity search capabilities of a vector store to facilitate retrieval
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 6})

from langchain_openai import ChatOpenAI

#initialize the LLM we'll use - OpenAI GPT 3.5 Turbo
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-0125")

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

# perform question answering with chat history
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)


question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(retriever_with_history, question_answer_chain)

from langchain_core.messages import HumanMessage

chat_history = []

print("\n--- Conversational RAG Turn 1 ---")
question = "What is Aetherfloris Ventus?"
print(f"Human: {question}")
ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": chat_history})
chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])
print(f"AI: {ai_msg_1['answer']}")

print("\n--- Conversational RAG Turn 2 ---")
second_question = "What does a single drop of it do?"
print(f"Human: {second_question}")
ai_msg_2 = rag_chain.invoke({"input": second_question, "chat_history": chat_history})
chat_history.extend([HumanMessage(content=second_question), ai_msg_2["answer"]])
print(f"AI: {ai_msg_2['answer']}")

print("\n--- Conversational RAG Turn 3 ---")
third_question = "How does it compare to Noctis Umbraherba?"
print(f"Human: {third_question}")
ai_msg_3 = rag_chain.invoke({"input": third_question, "chat_history": chat_history})
chat_history.extend([HumanMessage(content=third_question), ai_msg_3["answer"]])
print(f"AI: {ai_msg_3['answer']}")

print("\n--- Conversational RAG Turn 4 ---")
fourth_question = "Do you think the Biological section of the Voynich Manuscript is important?"
print(f"Human: {fourth_question}")
ai_msg_4 = rag_chain.invoke({"input": fourth_question, "chat_history": chat_history})
chat_history.extend([HumanMessage(content=fourth_question), ai_msg_4["answer"]])
print(f"AI: {ai_msg_4['answer']}")
