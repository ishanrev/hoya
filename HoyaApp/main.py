import os
import pandas as pd
import matplotlib.pyplot as plt
# from transformers import GPT2TokenizerFast
# from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import streamlit as st
from langchain_core.documents import Document

from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage



from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

st.title("Tester APP")

# search = st.text_input("Ask what youd like to ask")
search = st.text_input("whats my name")

OPENAI_API_KEY = "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"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def upload(chunks):
    # with open('parts.txt') as f:
    #     doc = f.read()

    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size = 512,
    #     chunk_overlap = 24,
    #     length_function = len
        
    # )
    # chunks = text_splitter.create_documents([doc])
    # print(chunks[0])
    
    # documents = [Document(content = text) for text in  chunks]
    # print(chunks)
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter( 
            )
    documents = text_splitter.create_documents(texts = chunks)
    print(documents)
    db = FAISS.from_documents(documents, embeddings)
    return db
# -------------------------------------------------


def createProcess(llm):

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("system", "Answer the following question based on the following context {context}"),
        ("human", "{input}")
    ]) 
    document_chain = create_stuff_documents_chain(llm, prompt )
    return document_chain


def create_retriever(db, document_chain, llm):

    retriever = db.as_retriever()

    retriever_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
       ("human", "Given are the previous conversation between you and the user and following context: {context}"),
       ("human", "give me a response to this question/statement: {input}")
    ])

    history_aware_retriever = create_history_aware_retriever(llm = llm, retriever = retriever, prompt = retriever_prompt)
    retrieval_chain = create_retrieval_chain(
        history_aware_retriever,
        document_chain    
    )
    
    retrieval_chain = create_retrieval_chain(retriever, document_chain)


    return retrieval_chain

# response = None
# chat_history = [
#     # HumanMessage(content="my name is bob"),

# ]
# if st.button('Submit'): 
    
#     print(search)
#     print(chat_history)
#     print("Uploading and restarting the process")
#     db = upload()
#     document_chain = createProcess()
#     retrieval_chain = create_retriever(db, document_chain)
#     response = retrieval_chain.invoke({
#         "chat_history": chat_history,
#         "input": search,
    
#     })
    
#     chat_history.append(HumanMessage(content=search))
#     chat_history.append(AIMessage(content = response["answer"]))
    
#     st.write(response["answer"])

# response = retrieval_chain.invoke({"input": "Who is John Doe"})
# print(response["answer"])


# APP






