
# Week 1: AI Fundamentals & Agentic AI Foundations
**CalderR Agentic AI Engineering Internship**  
*Timeline: Monday 22 June - Friday 26 June 2026*

This directory contains my completed daily labs, core assessments, and project submissions for Week 1 of the CalderR internship program.

---

## Weekly Projects (Category 1 & 2 Submissions)

### Intermediate Project: [To Be Chosen]
* **Description:** *Pending implementation*
* **Key Skills:** *Pending*
* **How to Run:** *Pending*

### Production Project: [To Be Chosen]
* **Description:** *Pending implementation*
* **Key Skills:** *Pending*
* **How to Run:** *Pending*

---

## Completed Labs Checklist

- [ ] **Lab 1.1: Your First Groq Agent**
  - Python CLI chatbot powered by `llama-3-8b` with continuous conversation memory, live token tracking, and custom `/clear` and `/exit` commands.
- [ ] **Lab 1.2: Manual ReAct Loop**
  - Frameworkless (no LangChain) implementation of a *Perceive ➔ Plan ➔ Act ➔ Observe* loop utilizing a mock facts database and custom math calculations.
- [ ] **Lab 1.3: Prompt Engineering A/B Test**
  - Automated or documented matrix testing 5 unique system prompts evaluating conciseness, accuracy, and tone variance.

---

## Weekly Self-Assessment Answers

### 1. Explain the difference between a language model and an agent. What capabilities does an agent add?
*Answer:* The traditional chatbot works on the one-turn input-output approach. It takes into account the user’s context, sends the same through the LLM for processing, and comes up with an output right away in the form of text. In the case of an Agentic loop, there is an execution process involving ReAct, which serves as the reasoning engine. The model evaluates the problem and picks some external tools (API, DB), analyzes the execution, and updates its plan in a number of hidden steps.

### 2. What is the 'context window' and why does it matter for agentic systems?
*Answer:* ReAct consists of making the LLM go through an iterative process of:
Thought ➔ Action ➔ Observation

Thought: The model understands the current situation and plans its next action.

Action: The model prepares a structured prompt in order to use the external tool.

Observation: The execution script invokes the tool and feeds the raw world data to the model.

That is extremely effective, because it makes complicated tasks modular and provides the LLM with up-to-date information, greatly cutting down hallucinations.

### 3. Describe the ReAct pattern. When would you use it versus a simple chain?
*Answer:* Context Window refers to the total number of tokens that the language model can process during an API request, including both the user prompt and the answer. Once the window is reached, the result is called context truncation, where the previous part of the conversation is simply truncated from memory. The agent either loses its memory, forgets instructions, ignores system prompts, or fails outright due to out-of-memory errors in the API request.

### 4. What is LCEL in LangChain? Write a 5-line example of a chain using the pipe operator.
*Answer:* The temperature regulates how random the selection of tokens is by the model.

Temperature = 0.0: Makes the model fully deterministic and forces it to always select the most probable token. Required when calling tools, dealing with structured responses (JSON/Regex parsing), or mathematical pipelines.

Temperature = 0.7+: Smoothes the probability curve, which allows selecting less probable tokens. Best for creative writing, brainstorming assistants, and multiple personas generation.

### 5. Explain the role of temperature in LLM sampling. When would you set it to 0?
*Answer:* The tokens are the smallest units of text (average length 4 characters or 0.75 words) that an LLM consumes and generates. Monitoring the number of tokens is important during production mainly because of the following reasons: Cost reduction (as the API of LLMs charges for the 1k/1M input/output tokens) and Reducing latency (as more number of tokens increases the response time).

### 6. Design a simple agent architecture for a customer support chatbot. What tools would it need?
*Answer:* The lack of the need for elaborate orchestration frameworks makes the engineer aware of the basics of state management, prompt boundaries, stop sequences, and handling errors of the API interface. Without that basic understanding, it will be impossible to debug or customize production agents failures, as the abstraction framework would eventually fail or cause delays.
