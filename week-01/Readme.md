
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
*Answer:* 

### 3. Describe the ReAct pattern. When would you use it versus a simple chain?
*Answer:* 

### 4. What is LCEL in LangChain? Write a 5-line example of a chain using the pipe operator.
*Answer:* 

### 5. Explain the role of temperature in LLM sampling. When would you set it to 0?
*Answer:* 

### 6. Design a simple agent architecture for a customer support chatbot. What tools would it need?
*Answer:*
