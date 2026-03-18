import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

# Initialize ChatOpenAI with OpenRouter configuration
chat = ChatOpenAI(
    model="stepfun/step-3.5-flash:free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    model_kwargs={
        "extra_headers": {
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Simple LangChain Script",
        }
    }
)

# Initialize conversation history with a system message
messages = [
    SystemMessage(content="You are a helpful and concise AI assistant."),
]

while True:
    try:
        user_input = input(">> ").strip()
    except (KeyboardInterrupt, EOFError):
        break

    if not user_input:
        continue

    if user_input.lower() in ("quit", "exit"):
        break

    messages.append(HumanMessage(content=user_input))

    try:
        response = chat.invoke(messages)
        assistant_reply = response.content
        print(f"\n {assistant_reply} \n")
        # Keep the assistant reply in history for multi-turn context
        from langchain_core.messages import AIMessage
        messages.append(AIMessage(content=assistant_reply))
    except Exception as e:
        print(f"\nError occurred: {e}\n")
        # Remove the last human message so the loop can continue cleanly
        messages.pop()
