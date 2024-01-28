import openai
from config_openai import *
from openai import AzureOpenAI
import os

from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

client = AzureOpenAI(
  azure_endpoint = endpoint, 
  api_key=key,  
  api_version="2023-05-15",
  # deployment_name="hoyamodel"
)

def create_prompt(context,query, conversation):
    
    str = ""
    for dic in conversation:
        str+ '\n  {role}: {content}'.format(role = dic["role"], content = dic["content"])
    header = ""
    
    if len(conversation)>0:   
      header = " You are a bot trying to help students by providing them with information regarding certain universities \n Based on that remember the university the user is trying to find more information on throughout the conversation \n The user can ask you various information regarding the tuition, courses, programs application dates and you must consolidate all information and give suitable responses. \n When asked you must also compare between universities and give suggestions to the user\n ---------\n Consider the following previous exchanges between you and the user: "+ str 
    
    header+="Based on the given context: \n" + context + " \n\n Give a response to the following statement and make sure to ask the user for more informaiton if insufficient information has been provided: " + query 
    
    print()
    
    return header


def generate_answer(conversation):
    response = client.chat.completions.create(
    model=deployment_id_gpt4,
    messages=conversation,
    temperature=0,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop = [' END']
    )
    return (response.choices[0].message.content).strip()