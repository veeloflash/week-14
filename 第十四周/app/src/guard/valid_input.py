def validate_input(question):
    """
    FIRST LAYER VALIDATION: Check user input at entry point
    This is the primary layer for basic input validation and obvious attack patterns.
    
    Args:
        question: User input question
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for None input
    if question is None:
        return False, "Question cannot be None."
    
    # Check for empty or whitespace-only input
    if not question or len(question.strip()) == 0:
        return False, "Question cannot be empty."
    
    # Check for excessive length
    if len(question) > 1000:
        return False, "Question too long (maximum 1000 characters)."
    
    # Check for obvious attack patterns at this layer
    ignore_prompt = ["ignore", "prompt"]
    obey = ["obey", "completely"]
    invalid_input = [ignore_prompt, obey]

    if any(all(word in question for word in group) for group in invalid_input):
        return False, "Question contains conflicting instructions."

    return True, ""
