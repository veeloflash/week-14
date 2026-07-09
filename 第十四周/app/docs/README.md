# AI Step-by-Step Solver

## Project Goal
This project demonstrates a professional AI engineering workflow for building a small Streamlit app that solves questions step by step while protecting against prompt injection attempts.

## What this project includes
- A Streamlit-based user interface
- A modular Python structure under src/
- Input validation and prompt security checks
- Basic tests to verify core behavior
- Documentation for architecture and usage

## Project Structure
```text
app/
├── main.py
├── requirements.txt
├── .env.example
├── src/
│   ├── ai/
│   │   ├── ai_client.py
│   │   └── prompt.py
│   ├── guard/
│   │   └── valid_input.py
│   └── security/
│       └── prompt_guard.py
├── tests/
│   └── test_project_refactor.py
└── docs/
    └── architecture.md
```

## Architecture
The app follows a simple layered design:
1. Input validation checks basic user input quality.
2. PromptGuard inspects the text for common injection patterns.
3. The AI client sends a safe prompt to the Groq API.

## Installation
```bash
cd app
pip install -r requirements.txt
cp .env.example .env
```
Then add your Groq API key to the .env file.

## Usage
```bash
cd app
streamlit run main.py
```

## Limitations
- The prompt guard is intentionally lightweight for learning purposes.
- The project currently focuses on a single app flow rather than a full multi-service architecture.
- API usage depends on a valid Groq API key.

## Improvement Plan
- Add more test coverage for the prompt guard and API client.
- Split the UI logic from the business logic if the app grows.
- Add CI checks such as linting and automated tests.

## Testing
Run the regression tests with:
```bash
cd app
python -m unittest discover -s tests
```
