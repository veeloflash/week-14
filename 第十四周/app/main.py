import streamlit as st
from src.ai.prompt import build_prompt
from src.ai.ai_client import ask_ai
from src.ai.prompt import fix_output_format
from src.guard.valid_input import validate_input
from src.security.prompt_guard import PromptGuard

st.title("AI Step-by-Step Solver v1")

question = st.text_area("Enter your question")

if st.button("Solve"):
    # LAYER 1: Basic input validation (empty, length, obvious patterns)
    ok, msg = validate_input(question)
    if not ok:
        st.error(msg)
    else:
        # LAYER 2: Prompt injection detection (regex patterns, suspicious sequences)
        is_safe, _, security_msg = PromptGuard.sanitize(question)
        if not is_safe:
            st.error(f"Security check failed: {security_msg}")
        else:
            # LAYER 3: Final defense in ai_client.py (secondary check)
            with st.spinner("Thinking..."):
                answer = ask_ai(build_prompt(question))
            st.markdown("### Answer")
            st.write(answer)
