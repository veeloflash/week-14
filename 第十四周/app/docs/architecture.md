# Architecture Overview

## Purpose
This document explains the folder layout and the responsibility of each module in the project.

## Module Responsibilities
- main.py: Streamlit entry point for the UI.
- src/ai/ai_client.py: Handles API communication and final safety checks.
- src/ai/prompt.py: Builds the structured prompt sent to the model.
- src/guard/valid_input.py: Validates the raw user input.
- src/security/prompt_guard.py: Detects suspicious or injection-style prompts.

## Design Notes
The project is organized so each module has a focused responsibility. This makes the system easier to review, extend, and maintain.
