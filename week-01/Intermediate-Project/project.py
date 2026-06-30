import os
import sys
import json
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Ensure the .env file is loaded correctly from root or local directory
env_path = Path('.') / '.env'
if not env_path.exists():
    env_path = Path('.').resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

if not os.getenv("GROQ_API_KEY"):
    print("❌ Error: GROQ_API_KEY not found.")
    sys.exit(1)

client = Groq()

# =====================================================================
# 1. THE EVALUATION DATASET
# =====================================================================
# We will test our prompts against raw inputs that need structured extraction
TEST_DATASET = [
    {
        "input": "My name is John Doe, my email is john@example.com and I need help with my account password.",
        "expected_keys": ["name", "email", "issue"]
    },
    {
        "input": "Urgent ticket from sarah.smith@techcorp.io: The main database server went down entirely at 4 PM.",
        "expected_keys": ["name", "email", "issue"]
    },
    {
        "input": "Hey, I am Alex (alex_99@gmail.com). Just wanted to say your tool is great! No support issues right now.",
        "expected_keys": ["name", "email", "issue"]
    }
]

# =====================================================================
# 2. THE SYSTEM PROMPT VARIANTS
# =====================================================================
# PROMPT A: A loose, basic instruction
PROMPT_A = """
Extract the customer's name, email, and support issue from the message. 
Return the output as a JSON object with keys: name, email, and issue.
"""

# PROMPT B: A highly defensive, structured instruction with negative constraints
PROMPT_B = """
You are a strict data extraction engine. Extract the following fields from the user message:
- name (If not found, set value to "UNKNOWN")
- email (If not found, set value to "UNKNOWN")
- issue (A brief summary of their technical problem. If no problem exists, set value to "NONE")

CRITICAL REQUIREMENT: You must output raw, valid JSON only. Do NOT wrap the JSON inside markdown code blocks (such as ```json ... ```). Do NOT include any conversational filler text before or after the JSON payload.
"""

# =====================================================================
# 3. PROGRAMMATIC GRADER METRICS
# =====================================================================
def evaluate_output(raw_output: str, expected_keys: list) -> dict:
    """Runs automated diagnostic assertions against the LLM's raw output string."""
    metrics = {
        "is_valid_json": False,
        "contains_markdown_blocks": "```" in raw_output,
        "has_all_keys": False,
        "total_score": 0
    }
    
    # Check if the output can be parsed as JSON
    try:
        clean_text = raw_output.strip()
        # Edge case: if the model wrapped it in markdown code blocks anyway, strip them for the backup check
        if clean_text.startswith("```"):
            clean_text = clean_text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            if clean_text.startswith("json"):
                clean_text = clean_text.split("\n", 1)[1].strip()

        parsed_json = json.loads(clean_text)
        metrics["is_valid_json"] = True
        
        # Verify that all required keys exist inside the parsed data
        metrics["has_all_keys"] = all(key in parsed_json for key in expected_keys)
    except Exception:
        pass
    
    # Calculate an objective score based on rules met
    if metrics["is_valid_json"]:
        metrics["total_score"] += 50
    if metrics["has_all_keys"]:
        metrics["total_score"] += 30
    if not metrics["contains_markdown_blocks"]:
        metrics["total_score"] += 20
        
    return metrics

# =====================================================================
# 4. EXECUTION PIPELINE RUNNER
# =====================================================================
def run_evaluation(prompt_name: str, system_prompt: str) -> list:
    print(f"🚀 Running Evaluation on Pipeline: {prompt_name}...")
    results = []
    
    for case in TEST_DATASET:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": case["input"]}
                ],
                temperature=0.0 # Strict token selection for reliability
            )
            raw_response = response.choices[0].message.content
            metrics = evaluate_output(raw_response, case["expected_keys"])
            results.append({
                "input": case["input"],
                "output": raw_response,
                "metrics": metrics
            })
        except Exception as e:
            print(f"Error executing evaluation case: {e}")
            
    return results

# =====================================================================
# 5. CONSOLIDATED CONSOLE REPORT GENERATOR
# =====================================================================
def main():
    results_a = run_evaluation("Prompt Variant A (Basic)", PROMPT_A)
    results_b = run_evaluation("Prompt Variant B (Defensive)", PROMPT_B)
    
    avg_score_a = sum(r["metrics"]["total_score"] for r in results_a) / len(results_a)
    avg_score_b = sum(r["metrics"]["total_score"] for r in results_b) / len(results_b)
    
    print("\n" + "="*60)
    print("PROMPT EVALUATION METRICS DASHBOARD")
    print("="*60)
    print(f"📊 Prompt Variant A Average Score: {avg_score_a:.2f} / 100")
    print(f"📊 Prompt Variant B Average Score: {avg_score_b:.2f} / 100")
    print("-"*60)
    
    print("\n📝 Detailed breakdown of Variant B's outputs:")
    for idx, res in enumerate(results_b):
        print(f"\n[Case {idx+1}] Input text: {res['input'][:40]}...")
        print(f"Raw Response: {res['output'].strip()}")
        print(f"Score Matrix -> Valid JSON: {res['metrics']['is_valid_json']} | Markdown Contained: {res['metrics']['contains_markdown_blocks']} | Score: {res['metrics']['total_score']}/100")

if __name__ == "__main__":
    main()
