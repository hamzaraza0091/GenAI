# 🤖 AI Code Review Bot

An intelligent, production-ready AI Code Review Bot built with **LangGraph**, **Google Gemini 3.6 Flash**, and **Streamlit**. 

## Features
- **Multi-Agent Architecture**: Separate specialized AI agents handle Bugs, Security, Code Quality, and Performance analysis independently.
- **Orchestrated by LangGraph**: Implements a structured, predictable workflow managing application state seamlessly.
- **Structured Output**: Relies strictly on Pydantic models to parse LLM outputs natively, preventing hallucinations and formatting errors.
- **Safe Execution**: Uses Python's built-in AST parsing to statically validate input. *Never executes user-submitted source code.*
- **Refactoring Engine**: Outputs completely synthesized, cleaned, and refactored code that addresses the issues found.

## Project Structure
```text
ai-code-review-bot/
├── app.py                  # Streamlit Frontend
├── graph.py                # LangGraph Orchestration & Nodes definition
├── schemas.py              # Pydantic structured output models
├── state.py                # LangGraph TypedDict state management
├── config.py               # Environment and LLM initialization
├── agents/                 # Individual LLM processing nodes
│   ├── bug_analyzer.py
│   ├── security_analyzer.py
│   ├── ...
└── utils/                  # Static code validation