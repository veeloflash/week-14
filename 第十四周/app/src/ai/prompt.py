def build_prompt(question):
    return f"""
You MUST follow this exact format. Do NOT add extra sections. Do NOT change titles.

1. Problem Understanding
2. Hint 1
3. Hint 2
4. Step-by-step Solution
5. Final Answer
6. Knowledge Summary

Question: {question}
"""
def fix_output_format(text: str):
    sections = [
        "1. Problem Understanding",
        "2. Hint 1",
        "3. Hint 2",
        "4. Step-by-step Solution",
        "5. Final Answer",
        "6. Knowledge Summary"
    ]

    fixed = {}
    current = None

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Detect section headers
        for sec in sections:
            if line.startswith(sec):
                current = sec
                fixed[current] = []
                break
        else:
            if current:
                fixed[current].append(line)

    # Build final output (fill missing sections)
    result = []
    for sec in sections:
        result.append(sec)
        if sec in fixed:
            result.extend(fixed[sec])
        else:
            result.append("(No content provided)")
        result.append("")  # blank line

    return "\n".join(result)
