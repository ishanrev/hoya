from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api

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

from main import *
from azure_openai import *
from config import *

from main import *

def ask(user_input, conversation):
    
    os.environ["AZURE_OPENAI_API_KEY"] = "3c0e63a717604bc196fc260cecffeea2"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://hoyaimain.openai.azure.com/"


    model = AzureChatOpenAI(
    openai_api_version="2023-05-15",
        azure_deployment="hoyamodel",
    )
    chat_history = []

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
    

    # results = [ doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") for doc in r]
    results = [doc[KB_FIELDS_SOURCEPAGE] + ": " + doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") for doc in r]
    content = "\n".join(results)
    
    print("*******************")
    print(conversation)

    # Here we make a conversational chatbot

    # references =[]
    # for result in results:
    #     references.append(result.split(":")[0])
    # st.markdown("### References:")
    # st.write(" , ".join(set(references)))

    prompt = create_prompt(content,user_input, conversation)            
    conversation.append({"role": "assistant", "content": prompt})
    # conversation.append({"role": "user", "content": user_input})
    reply = generate_answer(conversation)
    # conversation.append({"role": "assistant", "content": reply})

    return reply


app = Flask(__name__)
CORS(app, origins='*')  # Enable CORS for all routes
api = Api(app)

conversationGlobal = []

class HelloWorld(Resource):
    def get(self):
        return "hello world"
class Bot(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        question = json_data['question']
        conversation = json_data['conversation']
        
        print(question, conversation)
        
        response = ask(question, conversation) 
        
        return {"question": question, "response": response}
    
api.add_resource(HelloWorld, '/')
api.add_resource(Bot, '/ask')


if __name__ == '__main__':
    app.run(debug=True)