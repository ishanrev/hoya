import os
import argparse
import glob
import html
import io
import re
import time
from pypdf import PdfReader, PdfWriter
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import *
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from langchain.docstore.document import Document

from azure_openai import *
from main import *
from config import *

from main import *
os.environ["AZURE_OPENAI_API_KEY"] = "3c0e63a717604bc196fc260cecffeea2"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://hoyaimain.openai.azure.com/"

model = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="gpt-35-turbo",
)


import streamlit as st

st.header('Search Engine - Document')

user_input = st.text_input('Enter your question here:', 
                           'What are guard cells?')

chat_history = []

if st.button('Submit',key=1):

    # service_name = "YOUR-SEARCH-SERVICE-NAME"
    service_name = searchservice
    # key = "YOUR-SEARCH-SERVICE-ADMIN-API-KEY"
    key = searchkey

    endpoint = "https://{}.search.windows.net/".format(searchservice)
    index_name = index

    azure_credential =  AzureKeyCredential(key)

    # main llm client
    search_client = SearchClient(endpoint=endpoint,
                                        index_name=index_name,
                                        credential=azure_credential)
    # --------------------------

    KB_FIELDS_CONTENT = os.environ.get("KB_FIELDS_CONTENT") or "content"
    KB_FIELDS_CATEGORY = os.environ.get("KB_FIELDS_CATEGORY") or "category"
    KB_FIELDS_SOURCEPAGE = os.environ.get("KB_FIELDS_SOURCEPAGE") or "sourcepage"

    exclude_category = None
    skip = 0
    print("Searching:", user_input)
    print("-------------------")
    filter = "category ne '{}'".format(exclude_category.replace("'", "''")) if exclude_category else None
    r = search_client.search(user_input, 
                            # filter=filter,
                            # query_type=QueryType.SEMANTIC, 
                            # query_language="en-us", 
                            # query_speller="lexicon", 
                            # semantic_configuration_name="default", 
                            skip=skip,
                            top=3)
    
    print("/////////////////////////////////////////////////") 

    # results = [ doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") for doc in r]
    results = [doc[KB_FIELDS_SOURCEPAGE] + ": " + doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") for doc in r]
    content = "\n".join(results)
    # print(results)
    
    # content = "\n".join(results)


    # Here we make a conversational chatbot

    references =[]
    for result in results:
        references.append(result.split(":")[0])
    st.markdown("### References:")
    st.write(" , ".join(set(references)))

    conversation=[{"role": "system", "content": "Assistant is a great language model formed by OpenAI."}]
    prompt = create_prompt(content,user_input)            
    conversation.append({"role": "assistant", "content": prompt})
    conversation.append({"role": "user", "content": user_input})
    reply = generate_answer(conversation)

    st.markdown("### Answer is:")
    st.write(reply)
    
    # langchain conversational chatbot
    
    # references =[]
    # for result in results:
    #     references.append("hi")
    # st.markdown("### References:")
    # st.write(" , ".join(set(references)))
    
    # db = upload(results)
    # print(type(db))
    # document_chain = createProcess( llm = model) 
    # print(type(document_chain)) 
    # retrieval_chain = create_retriever(db, document_chain, llm = model)  
    # print(type(retrieval_chain))
    
    # response = document_chain.invoke({
    # "input": "how can langsmith help with testing?",
    # "context": [Document(page_content="langsmith can let you visualize test results")]
    # })
    
    # message = HumanMessage(
    #     content="Translate this sentence from English to French. I love programming."
    # )
    # model([message])



    # response = retrieval_chain.invoke({"input": user_input})
    # print(response)
    # chat_history.append(HumanMessage(content= user_input))
    # chat_history.append(AIMessage(content= response))
    
    # st.write(response["answer"])
    
