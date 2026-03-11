from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import LLMChain
import os # for system interactions
from dotenv import load_dotenv, find_dotenv # to manage env variables

load_dotenv(find_dotenv()) # search and load env file upwards in file tree, from current directory

# Grab API Key ( as named in .env)
api_key = os.environ["GEMINI_API"]  

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.7)

# Define a template for the prompt
template = """You are a helpful assistant. 

Chat History:
{history}

User: {user_input}
Assistant:"""

# Create a prompt template
prompt = PromptTemplate(
    input_variables=["history", "user_input"],
    template=template
)

# Initialize memory to store conversation history
memory = ConversationBufferMemory(
    memory_key="history",
    input_key="user_input"
)

# Create the chain with memory
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=False
)

# Simple chat loop
def chat():
    print("Chat with Gemini (type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Get response from chain
        response = chain.invoke({"user_input": user_input})
        print(f"Assistant: {response['text']}\n")

if __name__ == "__main__":
    chat()
