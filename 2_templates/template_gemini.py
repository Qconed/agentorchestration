import os # for system interactions
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv # to manage env variables

# reference: https://www.philschmid.de/gemini-langchain-cheatsheet

load_dotenv(find_dotenv()) # search and load env file upwards in file tree, from current directory

# Grab API Key ( as named in .env)
api_key = os.environ["GEMINI_API"]

import os # for system interactions
import sys
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv(find_dotenv()) # search and load env file upwards in file tree, from current directory

# Grab API Key ( as named in .env)
api_key = os.environ["GEMINI_API"]

if not api_key:
    print("api key not found")
    sys.exit(1)

# Initialize model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0,
)
 
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "{input}"),
])
 
chain = prompt | llm
result = chain.invoke({
    "input_language": "English",
    "output_language": "French",
    "input": "I love programming.",
})
print(result.content) 