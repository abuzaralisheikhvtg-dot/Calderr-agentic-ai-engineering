import streamlit as st
import os
import re
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

# =====================================================================
# 1. SETUP & CONFIGURATION
# =====================================================================
# Page config must be the first Streamlit command
st.set_page_config(page_title="Agentic Research Assistant", page_icon="🤖", layout="centered")

# Load Environment Variables
env_path = Path('.') / '.env'
if not env_path.exists():
    env_path = Path('.').resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ Error: GROQ_API_KEY not found in .env file.")
    st.stop()

client = Groq(api_key=api_key)

# =====================================================================
# 2. THE TOOLS (MOCK EXTERNAL APIs)
# =====================================================================
def search_knowledge_base(query: str) -> str:
    """Mock search engine for the agent to look up facts."""
    q = query.lower()
    
    # Expanded keywords to catch variations in the agent's search queries
    if "ceo" in q or "alex" in q:
        return "The CEO of CalderR is Alex Calder, Age: 34."
    elif "revenue" in q or "q3" in q or "financial" in q or "earnings" in q:
        return "CalderR's Q3 revenue was $4.2 million."
    elif "calderr" in q:
        return "CalderR is an elite Agentic AI engineering firm."
        
    return f"Search results for '{query}': No specific highly-relevant data found, general web results suggest standard definitions."

def calculate_math(expression: str) -> str:
    """Safe math evaluator tool."""
    try:
        # Strip out alphabetical characters for safety before evaluating
        safe_expr = re.sub(r'[^0-9+\-*/(). ]', '', expression)
        if safe_expr:
            result = eval(safe_expr)
            return str(result)
        return "Invalid math expression."
    except Exception as e:
        return f"Calculation error: {str(e)}"

# Dictionary to map tool names to actual functions
AVAILABLE_TOOLS = {
    "search_db": search_knowledge_base,
    "calculate": calculate_math
}

# =====================================================================
# 3. THE SYSTEM PROMPT & REACT LOOP LOGIC
# =====================================================================
SYSTEM_PROMPT = """
You are an autonomous Research Assistant.
You must solve the user's request by utilizing your tools.

CRITICAL INSTRUCTION: You must NEVER answer based on your own pre-existing knowledge. You must ALWAYS use the search_db tool to look up information about companies, people, or facts before generating a Final Answer.

You have access to the following tools:
1. search_db: Use this to search the internet or knowledge base for facts, names, and data. (Action Input must be a search string)
2. calculate: Use this to perform math calculations. (Action Input must be a valid math expression like 20 * 4)

You MUST use the following exact format for your responses:

Thought: [Explain your reasoning step-by-step]
Action: [The name of the tool to use: either search_db or calculate]
Action Input: [The exact input for the tool]

(Stop generating and wait for the Observation)

Once you have gathered enough information to answer the user's request, use this exact format:
Thought: I have all the information I need.
Final Answer: [Your final synthesized response to the user]
"""

def run_agent(user_query: str):
    """Executes the ReAct loop and yields UI updates to Streamlit."""
    
    # Initialize the memory for this specific task
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    step_count = 0
    max_steps = 6 # Guardrail to prevent infinite loops
    
    # We use st.status to show a cool "thinking" spinner in the UI
    with st.status("Agent is thinking and researching...", expanded=True) as status:
        
        while step_count < max_steps:
            step_count += 1
            
            # 1. Call the LLM with a hard Stop Sequence
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.0,
                stop=["Observation:"] # Force the model to yield back to Python
            )
            
            llm_output = response.choices[0].message.content.strip()
            messages.append({"role": "assistant", "content": llm_output})
            
            # 2. Check if the LLM reached a Final Answer
            if "Final Answer:" in llm_output:
                final_answer = llm_output.split("Final Answer:")[-1].strip()
                status.update(label="Research Complete!", state="complete", expanded=False)
                return final_answer
            
            # 3. Parse the Tool Request
            thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|$)", llm_output, re.DOTALL)
            action_match = re.search(r"Action:\s*(.*?)\n", llm_output)
            action_input_match = re.search(r"Action Input:\s*(.*)", llm_output)
            
            if thought_match:
                st.write(f"🧠 **Thought:** {thought_match.group(1).strip()}")
                
            if action_match and action_input_match:
                action_name = action_match.group(1).strip()
                action_input = action_input_match.group(1).strip()
                
                st.write(f"🛠️ **Action:** `{action_name}` | **Input:** `{action_input}`")
                
                # 4. Execute the tool
                if action_name in AVAILABLE_TOOLS:
                    observation = AVAILABLE_TOOLS[action_name](action_input)
                else:
                    observation = f"Error: Tool '{action_name}' not found."
                    
                st.write(f"🔍 **Observation:** {observation}")
                st.divider() # Visual separator
                
                # Feed the real-world observation back to the LLM
                messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                # Fallback if the LLM breaks formatting
                status.update(label="Agent encountered a formatting error.", state="error")
                return "The agent failed to format its response correctly. Please try again."
                
        status.update(label="Agent timed out.", state="error")
        return "The agent reached the maximum number of steps without finding an answer."

# =====================================================================
# 4. STREAMLIT USER INTERFACE
# =====================================================================
st.title("🤖 Agentic Research Assistant")
st.markdown("Ask me complex questions! I will dynamically search databases and calculate math to find your answer.")

# Initialize chat history in session state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Display previous chat history
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input block
if user_prompt := st.chat_input("E.g., Who is the CEO of CalderR and what is 15% of their age?"):
    
    # Render user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
    
    # Render assistant response block
    with st.chat_message("assistant"):
        # Run the agentic loop
        final_output = run_agent(user_prompt)
        
        # Display the final synthesized answer
        st.markdown(f"**Final Answer:** {final_output}")
        
    st.session_state.chat_messages.append({"role": "assistant", "content": final_output})
