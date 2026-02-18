import os # for system interactions
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv # to manage env variables

load_dotenv(find_dotenv()) # search and load env file upwards in file tree, from current directory

# Grab API Key ( as named in .env)
api_key = os.environ["GEMINI_API"]

# Initialize the model
# Use "gemini-2.0-flash" for speed or "gemini-1.5-pro" for complex reasoning
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0.7
)
print("asking question...")
response = llm.invoke("What are the three most important concepts in functional programming?")
print(response.content)