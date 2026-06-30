Automated Prompt Engineering Evaluator 🚀

An engineering-grade, quantitative testing pipeline that programmatically evaluates, benchmarks, and scores different LLM system prompt variations. This framework moves prompt engineering from a subjective "guess-and-check" process to a deterministic, metrics-driven pipeline.

📋 Table of Contents

Core Architecture

Evaluation Metrics & Scoring

Setup & Installation Instructions

How to Run

Analysis of Results

🧠 Core Architecture

When deploying Large Language Models (LLMs) to production pipelines, slight variations in prompts can result in dramatic failures (such as syntax errors during JSON parsing). This project sets up an automated testing suite using the Groq API and the state-of-the-art llama-3.1-8b-instant model.

The evaluator splits the testing process into four architectural pillars:

The Prompts: Two distinct system prompts (Variant A is basic, Variant B is highly structured and defensive).

The Dataset: A static test set with raw, unformatted messages containing different extraction edge cases.

The Grader Engine: Programmatic assertion metrics that run deterministic Python checks on the raw string output.

The Dashboard Reporter: Aggregates scores and outputs a readable comparative performance report.

📊 Evaluation Metrics & Scoring

Each output is evaluated out of a maximum of 100 points based on strict criteria:

Metric

Score Weight

Description

JSON Parseability

50 pts

Verifies if the output string can be parsed successfully by Python's native json.loads().

Schema Completeness

30 pts

Assures all expected keys (name, email, issue) exist inside the parsed payload.

No Markdown Blocks

20 pts

Penalizes the model if it wraps JSON in markdown code blocks (```json ... ```), which breaks automated parsing pipelines.

🛠️ Setup & Installation Instructions

Prerequisites

Python 3.10 or higher installed.

An active Groq API Key (Get one at console.groq.com).

Step 1: Clone and Navigate

Ensure you are in the correct sub-directory inside your repository:

cd week-01


Step 2: Set Up Virtual Environment

Ensure your virtual environment is active. If not, spin it up and activate it:

# Windows PowerShell
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate


Step 3: Install Dependencies

Install the required Groq and environment loading libraries:

pip install -r requirements.txt


Step 4: Configure Environment Variables

Create a .env file in the root of your project or inside the week-01 directory:

GROQ_API_KEY=gsk_your_actual_groq_key_here


🏃‍♂️ How to Run

Execute the pipeline runner from your terminal:

python labs/project_1_intermediate.py


📈 Analysis of Results

Upon completion, you will see a console dashboard showing a clear comparison of the two prompt strategies:

============================================================
PROMPT EVALUATION METRICS DASHBOARD
============================================================
📊 Prompt Variant A Average Score: 26.67 / 100
📊 Prompt Variant B Average Score: 100.00 / 100
------------------------------------------------------------


Key Takeaways

Defensive Design Matters: Variant A (loose styling) fails because the LLM naturally tries to hold a conversation, inserting markdown wrappers and greetings that crash parsers.

Deterministic Token Selection: Running the evaluation at temperature=0.0 ensures absolute repeatability across test runs.

Graceful Fallbacks: Specifying fallback strategies inside the system instructions (such as returning NONE for issues) guarantees complete schema consistency even when data is missing.
