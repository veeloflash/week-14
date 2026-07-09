import streamlit as st

from src.ai.ai_client import ask_ai
from src.ai.prompt import build_prompt
from src.guard.valid_input import validate_input
from src.security.prompt_guard import PromptGuard

st.set_page_config(page_title="AI Step-by-Step Solver", page_icon="🧠", layout="centered")
st.title("AI Step-by-Step Solver")
st.caption("A refactored engineering-style demo with validation, prompt protection, and clear module boundaries.")

question = st.text_area("Enter your question")

if st.button("Solve"):
    ok, msg = validate_input(question)
    if not ok:
        st.error(msg)
    else:
        is_safe, _, security_msg = PromptGuard.sanitize(question)
        if not is_safe:
            st.error(f"Security check failed: {security_msg}")
        else:
            with st.spinner("Thinking..."):
                answer = ask_ai(build_prompt(question))
            st.markdown("### Answer")
            st.write(answer)
