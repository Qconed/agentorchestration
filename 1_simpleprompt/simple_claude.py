import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def main():
    api_key = os.getenv("CLAUDE_API")
    
    if not api_key:
        print("Error: CLAUDE_API not found in .env file.")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter your prompt for Claude: ")

    if not prompt:
        print("Error: No prompt provided.")
        sys.exit(1)

    print(f"\nSending prompt to Claude (claude-sonnet-4-6)...")

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        print("\n--- Claude Response ---")
        print(message.content[0].text)
        print("-----------------------")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
