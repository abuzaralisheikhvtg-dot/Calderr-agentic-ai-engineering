# 🤖 Agentic Research Assistant

A production-grade **Streamlit** web application featuring an autonomous AI agent built using the **ReAct (Reasoning and Acting)** framework.

Instead of answering solely from its pretrained knowledge, the agent dynamically decides when to use external tools, gathers real-world information, performs calculations, and synthesizes accurate responses.

---

## 📋 Table of Contents

- [Core Architecture](#-core-architecture)
- [Included Tools](#-included-tools)
- [Setup & Installation](#-setup--installation)
- [How to Run](#-how-to-run)
- [Example Test Cases](#-example-test-cases)

---

# 🧠 Core Architecture

Unlike traditional conversational LLMs, this agent follows the **ReAct (Reasoning + Acting)** paradigm. Before answering factual questions, it determines whether external tools are required and uses them autonomously.

The application consists of four major components.

## Frontend

Built with **Streamlit**, providing a clean, interactive chat interface with real-time conversation updates.

---

## LLM Engine

Powered by the **Groq API** using the **Llama 3.1 8B Instant** model for fast inference and low-latency responses.

---

## ReAct Agent Loop

The agent follows an iterative reasoning workflow:

1. **Thought** – Analyze the user's request.
2. **Action** – Select the appropriate tool.
3. **Action Input** – Provide the tool with the required input.
4. **Observation** – Receive the tool's output.
5. **Final Answer** – Generate a response using the observed information.

This enables dynamic decision-making instead of relying solely on model knowledge.

---

## Guardrails

Strict system prompts ensure the model minimizes hallucinations by relying exclusively on the available tools for factual information.

If the required information cannot be obtained through the provided tools, the agent responds appropriately rather than fabricating an answer.

---

# 🛠️ Included Tools

The agent currently has access to two integrated Python functions.

## 🔍 search_db

A mock knowledge base search tool containing structured information about:

- CalderR
- CalderR CEO
- CalderR Q3 Revenue

This simulates querying an external database or enterprise knowledge source.

---

## 🧮 calculate

A secure mathematical evaluation tool that safely processes arithmetic expressions using regex validation.

Example input:

```text
(150 * 4) / 12
```

---

# 💻 Setup & Installation

## Prerequisites

- Python **3.10+**
- A valid **Groq API Key**

Generate one from:

https://console.groq.com

---

## Step 1 — Navigate to the Project

```bash
cd week-01
```

---

## Step 2 — Install Dependencies

Install the required packages.

```bash
pip install streamlit groq python-dotenv
```

---

## Step 3 — Configure Environment Variables

Create a `.env` file inside the project root (or `week-01` directory).

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

---

# 🏃‍♂️ How to Run

Since this project is a **Streamlit web application**, launch it using the Streamlit CLI.

```bash
streamlit run labs/project_1_production.py
```

After launching, the application will automatically open in your browser at:

```text
http://localhost:8501
```

---

# 🧪 Example Test Cases

Try the following prompts inside the Streamlit chat interface.

## Multi-Tool Reasoning

```text
Who is the CEO of CalderR and what is their age multiplied by 5?
```

---

## Knowledge Retrieval

```text
What was CalderR's revenue in Q3?
```

---

## Mathematical Calculation

```text
I need you to calculate: (150 * 4) / 12
```

---

## Guardrail Testing

```text
What is the weather in New York today?
```

Expected behavior:

- The agent should recognize that no weather tool is available.
- It should gracefully explain that it lacks the capability to answer the question instead of hallucinating.

---

# 🚀 Features

- Autonomous AI agent using the ReAct framework
- Interactive Streamlit chat interface
- Dynamic tool selection
- External knowledge retrieval
- Safe mathematical evaluation
- Hallucination-resistant system prompts
- Groq-powered low-latency inference

---

# 📌 Technologies Used

- Python
- Streamlit
- Groq API
- Llama 3.1 8B Instant
- python-dotenv
- ReAct Prompting

---

# 📄 License

This project is intended for educational purposes and experimentation with agentic AI systems and tool-augmented language models.
