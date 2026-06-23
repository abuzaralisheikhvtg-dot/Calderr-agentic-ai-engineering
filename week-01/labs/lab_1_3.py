import sys
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# 5 distinct system prompts testing tone, accuracy, and conciseness
SYSTEM_PROMPTS = [
    "You are a helpful, factual AI assistant. Provide a clear and neutral answer.",
    "You are an expert AI researcher. Use highly technical language, academic jargon, and a formal tone.",
    "You are a Gen-Z TikTok influencer. Explain this using modern slang, emojis, and keep it extremely brief.",
    "You are a cynical, grumpy robot who hates answering questions but does it anyway. Be concise and sarcastic.",
    "You are a kindergarten teacher. Explain this using very simple words and a fun, childlike analogy."
]

# The baseline query we will test against all 5 prompts
TEST_QUERY = "Explain the difference between a standard Large Language Model (LLM) and an Agentic AI system."

def main():
    try:
        client = Groq()
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        sys.exit(1)

    print("=" * 50)
    print("Running Prompt A/B Testing Matrix (5 Prompts)")
    print("=" * 50 + "\n")

    results = []

    for i, prompt in enumerate(SYSTEM_PROMPTS, 1):
        print(f"Testing Persona {i}/5...")
        
        response = client.chat.completions.create(
            model="llama-3-8b-8192",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": TEST_QUERY}
            ],
            temperature=0.7 # Standard variance to allow tone to shine
        )
        
        reply = response.choices[0].message.content
        results.append((prompt, reply))

    # Auto-generate the documentation required by the internship
    print("\nGenerating Markdown Report...")
    with open("lab_1_3_results.md", "w", encoding="utf-8") as f:
        f.write("# Lab 1.3: Prompt Engineering A/B Test Results\n\n")
        f.write(f"**Test Query:** *\"{TEST_QUERY}\"*\n\n---\n\n")
        
        for i, (prompt, reply) in enumerate(results, 1):
            f.write(f"### Persona {i}\n")
            f.write(f"**System Prompt:** `{prompt}`\n\n")
            f.write(f"**Output:**\n{reply}\n\n")
            f.write("---\n\n")

    print("Testing complete! Check 'lab_1_3_results.md' for your documented findings.")

if __name__ == "__main__":
    main()
