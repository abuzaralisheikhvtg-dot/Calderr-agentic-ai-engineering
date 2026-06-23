import os
import sys
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def main():
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found.")
        print(f"Looked at: {Path('.').resolve() / '.env'}")
        print(f"And looked at: {Path('.').resolve().parent / '.env'}")
        sys.exit(1)

    try:
        client = Groq()
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        sys.exit(1)

    try:
        client = Groq()
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        sys.exit(1)

    history = [
        {"role": "system", "content": "You are a helpful, brilliant, and concise AI Assistant."}
    ]
    
    print("=" * 50)
    print("Groq CLI Chatbot Initialized")
    print("Commands: /clear to reset history, /exit to quit")
    print("=" * 50 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() == '/exit':
                print("\nShutting down safely.")
                break
                
            if user_input.lower() == '/clear':
                history = [history[0]]
                print("\nChat history cleared.\n")
                continue

            history.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=history,
                temperature=0.7
            )

            reply = response.choices[0].message.content
            usage = response.usage

            history.append({"role": "assistant", "content": reply})

            print(f"\nAgent: {reply}\n")
            print(f" Prompt: {usage.prompt_tokens} | Completion: {usage.completion_tokens} | Total: {usage.total_tokens}")
            print("-" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Exiting.")
            break
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()
