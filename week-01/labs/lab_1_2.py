import sys
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Mock database required by the lab
FACTS_DB = {
    "calderr": "CalderR is an elite Agentic AI engineering firm.",
    "ceo": "The CEO of CalderR is Jane Doe.",
    "internship": "The CalderR internship program focuses on agentic systems."
}

"""def search_db(query):
    query = query.lower()
    for key, fact in FACTS_DB.items():
        if key in query:
            return fact
    return "No information found in database."""

def search_db(query: str) -> str:
    # Convert query to lowercase to prevent capitalization bugs
    q = query.lower()
    
    # A smart mock database dictionary
    mock_data = {
        "ceo": "The CEO of CalderR is Alex Calder, Age: 34.",
        "calderr ceo": "The CEO of CalderR is Alex Calder, Age: 34.",
        "leadership": "CalderR is led by Alex Calder (CEO, Age: 34) and their core AI research team.",
        "alex calder": "Alex Calder is the CEO of CalderR, aged 34 years old."
    }
    
    # Check if any of our keywords are hidden inside the agent's search query
    for key in mock_data:
        if key in q:
            return mock_data[key]
            
    # Default fallback if it searches for something completely random
    return "CalderR is an elite Agentic AI engineering firm."

def calculate(expression):
    try:
        # Note: eval() is unsafe in real production, but strictly required by Lab 1.2
        return str(eval(expression))
    except Exception as e:
        return f"Error calculating: {e}"

def execute_tool(action, action_input):
    if action == "search_db":
        return search_db(action_input)
    elif action == "calculate":
        return calculate(action_input)
    return f"Unknown tool: {action}"

system_prompt = """
You are an AI agent that runs in a loop of Thought, Action, Action Input, Observation.
Use the tools available to answer the user's question.

Available Tools:
- search_db: Search a database of facts. Input: a simple keyword or search query.
- calculate: Evaluate a math expression. Input: a mathematical string (e.g., '2 + 2').

Format your response strictly as follows:
Thought: <reasoning about what to do next>
Action: <tool name>
Action Input: <input for the tool>

If you have the final answer, use this format instead:
Thought: <reasoning>
Final Answer: <the answer to the user>
"""

def main():
    try:
        client = Groq()
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        sys.exit(1)

    print("=" * 50)
    print("Manual ReAct Agent Loop")
    print("Try asking: 'Who is the CEO of CalderR and what is 25 * 4?'")
    print("=" * 50 + "\n")

    user_input = input("Question: ").strip()
    if not user_input:
        return

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    # ReAct Loop (max 5 iterations to prevent infinite loops)
    for step in range(5):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.0 # Zero temperature is crucial for reliable tool calling formatting
        )
        
        reply = response.choices[0].message.content
        print(f"\n--- Agent Loop Step {step + 1} ---")
        print(reply)
        
        messages.append({"role": "assistant", "content": reply})

        if "Final Answer:" in reply:
            print("\nTask Complete.")
            break

        # Parse the agent's chosen action and input
        action_match = re.search(r"Action:\s*(.*)", reply)
        input_match = re.search(r"Action Input:\s*(.*)", reply)

        if action_match and input_match:
            action = action_match.group(1).strip()
            action_input = input_match.group(1).strip()
            
            print(f"\nExecuting Tool: {action}('{action_input}')")
            observation = execute_tool(action, action_input)
            print(f"Observation: {observation}")
            
            # Feed the observation back to the LLM
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            print("\nAgent formatting error. Nudging it to fix.")
            messages.append({"role": "user", "content": "Observation: You must format your response with Action and Action Input, or use Final Answer."})

if __name__ == "__main__":
    main()
