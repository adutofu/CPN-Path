# CPN-Path

CPN-Path is a Python-based AI experimentation and prompt evaluation project built around the Anthropic Claude API. The project demonstrates how to:
- send user prompts to a language model,
- maintain conversational history,
- generate structured responses,
- evaluate prompt quality using a dataset,
- and produce a prompt evaluation report.

This repository is designed for exploring AI-assisted problem solving, prompt engineering, and structured response validation in a simple, lightweight Python workflow.

## Overview

This project includes:
- a chatbot interface powered by the Anthropic Messages API,
- reusable chat helper functions,
- prompt evaluation logic for generated outputs,
- dataset-driven scoring for model responses,
- and report generation for summarizing evaluation results.

The project is useful for learning and testing:
- LLM interaction patterns,
- prompt design,
- structured response generation,
- validation of Python, JSON, and Regex outputs,
- AI-as-a-judge evaluation workflows.

## Features

- Chatbot integration with Anthropic Claude
- Multi-turn conversation tracking
- Simple message builder helpers
- Prompt evaluation pipeline
- Syntax validation for generated code
- JSON-based dataset evaluation
- Summary report generation
- AWS-related example tasks for Python, JSON, and regex generation

## Repository Structure

```text
CPN-Path/
├── chat_bot.py
├── chat_functions.py
├── class PromtEvaluator.py
├── dataset.json
├── main.py
├── promt_evaluation.py
├── structured_data_exercise.py
├── .gitignore
└── README.md
