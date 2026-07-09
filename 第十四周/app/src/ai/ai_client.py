import os
from typing import List, Dict

import requests
from dotenv import load_dotenv

from src.ai.prompt import fix_output_format
from src.security.prompt_guard import PromptGuard

load_dotenv()

conversation_history: List[Dict[str, str]] = []


def get_api_key() -> str:
    """Read the Groq API key from the environment without crashing at import time."""
    return os.getenv("GROQ_API_KEY", "").strip()


def ask_ai(prompt: str) -> str:
    """
    Send prompt to Groq API and get AI response with security & error handling.

    The input should already be validated by validate_input() and PromptGuard.sanitize(),
    but we perform a final safety check here as a secondary defense measure.
    """
    if not prompt or not isinstance(prompt, str):
        return "[Input Error] Prompt must be a non-empty string"

    is_safe, sanitized_prompt, error_msg = PromptGuard.sanitize(prompt)
    if not is_safe:
        return f"[Security Threat] {error_msg}"

    api_key = get_api_key()
    if not api_key:
        return "[Configuration Error] GROQ_API_KEY is not set. Please add it to your .env file."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    conversation_history.append({"role": "user", "content": sanitized_prompt})

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": conversation_history
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as exc:
        return f"[System Error] {str(exc)}"

    try:
        data = response.json()
    except ValueError:
        return "[Parse Error] Invalid JSON response from API"

    if "choices" not in data or not data["choices"]:
        return f"[API Error] No response choices in data: {data}"

    try:
        ai_reply = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return "[Parse Error] Could not extract message from response"

    ai_reply = fix_output_format(ai_reply)
    conversation_history.append({"role": "assistant", "content": ai_reply})

    return ai_reply
