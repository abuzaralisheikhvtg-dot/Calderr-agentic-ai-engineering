# 🚀 Automated Prompt Engineering Evaluator

An engineering-grade, quantitative testing pipeline that programmatically evaluates, benchmarks, and scores different LLM system prompt variations.

Instead of relying on subjective "guess-and-check" prompt engineering, this project introduces a deterministic, metrics-driven evaluation framework that measures prompt quality using automated scoring.

---

## 📋 Table of Contents

- [Core Architecture](#-core-architecture)
- [Evaluation Metrics & Scoring](#-evaluation-metrics--scoring)
- [Setup & Installation](#-setup--installation)
- [How to Run](#-how-to-run)
- [Sample Results](#-sample-results)
- [Key Takeaways](#-key-takeaways)

---

# 🧠 Core Architecture

When deploying Large Language Models (LLMs) into production, even small prompt changes can dramatically affect reliability. One common failure is generating responses that break downstream JSON parsers.

This project builds an automated evaluation pipeline using:

- **Groq API**
- **Llama 3.1 8B Instant**
- **Python**
- **Deterministic evaluation metrics**

The framework consists of four architectural components.

## 1. Prompt Variants

Two different system prompts are evaluated.

- **Variant A** — Simple, minimal instructions.
- **Variant B** — Highly structured, defensive prompt engineering.

---

## 2. Evaluation Dataset

A fixed dataset containing raw customer messages with various extraction edge cases.

Examples include:

- Missing information
- Multiple emails
- Ambiguous issues
- Irregular formatting

---

## 3. Grading Engine

Each model response is automatically validated using deterministic Python assertions.

No human judgment is required.

---

## 4. Dashboard Reporter

The final stage aggregates all scores and produces a side-by-side comparison of each prompt variant.

---

# 📊 Evaluation Metrics & Scoring

Every generated response is scored out of **100 points**.

| Metric | Weight | Description |
|---------|--------|-------------|
| JSON Parseability | **50 pts** | Verifies that the output can be parsed successfully using Python's `json.loads()` |
| Schema Completeness | **30 pts** | Confirms that all required fields (`name`, `email`, `issue`) exist |
| No Markdown Blocks | **20 pts** | Penalizes outputs wrapped inside ```json ... ``` code fences |

---

# 🛠️ Setup & Installation

## Prerequisites

- Python **3.10+**
- A valid **Groq API Key**

You can generate one from:

https://console.groq.com

---

## Step 1 — Navigate to the Project

```bash
cd week-01
```

---

## Step 2 — Activate Virtual Environment

### Windows (PowerShell)

```powershell
.\venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Configure Environment Variables

Create a `.env` file inside the project root.

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

---

# 🏃‍♂️ How to Run

Execute the evaluation pipeline.

```bash
python labs/project_1_intermediate.py
```

---

# 📈 Sample Results

After execution, you'll see a dashboard similar to:

```text
============================================================
PROMPT EVALUATION METRICS DASHBOARD
============================================================

📊 Prompt Variant A Average Score: 26.67 / 100

📊 Prompt Variant B Average Score: 100.00 / 100

------------------------------------------------------------
```

---

# 🎯 Key Takeaways

### Defensive Prompt Design

Variant A performs poorly because the model naturally adds greetings, explanations, or Markdown formatting that break downstream parsers.

---

### Deterministic Generation

Using **temperature = 0.0** ensures identical outputs across repeated evaluation runs, making benchmarking reproducible.

---

### Schema Reliability

Embedding fallback instructions (such as returning `"NONE"` for missing values) guarantees consistent JSON schemas even when user input is incomplete.

---

# 📌 Technologies Used

- Python
- Groq API
- Llama 3.1 8B Instant
- JSON
- python-dotenv

---

# 📄 License

This project is intended for educational and prompt engineering experimentation.
