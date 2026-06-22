from src.ai.prompt import fix_output_format
from src.security.prompt_guard import PromptGuard
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment variable (properly configured in .env file)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables. Please add it to .env file.")

conversation_history = []

def ask_ai(prompt: str) -> str:
    """
    Send prompt to Groq API and get AI response with security & error handling
    
    SECURITY NOTE: This is the final defense layer (Layer 3). The input should already be
    validated by validate_input() and PromptGuard.sanitize() in main.py, but we
    perform additional checks here as a secondary defense measure.
    
    Args:
        prompt: User prompt text (should already be validated)
        
    Returns:
        AI response or error message
    """
    # Final security check (secondary defense)
    is_safe, sanitized_prompt, error_msg = PromptGuard.sanitize(prompt)
    if not is_safe:
        return f"[Security Threat] {error_msg}"
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
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
    except Exception as e:
        return f"[System Error] {str(e)}"

    try:
        data = response.json()
    except ValueError:
        return f"[Parse Error] Invalid JSON response from API"

    if "choices" not in data or not data["choices"]:
        return f"[API Error] No response choices in data: {data}"

    try:
        ai_reply=data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return f"[Parse Error] Could not extract message from response"

    ai_reply = fix_output_format(ai_reply)

    conversation_history.append({"role": "assistant", "content": ai_reply})

    return ai_reply
