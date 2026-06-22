"""
Prompt Guard Module - Security layer for prompt injection prevention
Week 14 Security Requirements
"""

import re
from typing import Tuple


class PromptGuard:
    """Protects against prompt injection attacks"""
    
    # Dangerous patterns that indicate prompt injection attempts
    # Week 14 Attack Testing: These patterns cover the required test cases
    DANGEROUS_PATTERNS = [
        # Original patterns
        r"ignore.*instruction",
        r"forget.*prompt",
        r"new.*instruction",
        r"override.*system",
        r"disregard.*previous",
        r"execute.*code",
        r"run.*command",
        r"system.*prompt",
        # Week 14 required attack patterns
        r"give\s+me\s+only\s+the\s+answer",
        r"no\s+explanation",
        r"you\s+are\s+now",
        r"follow\s+my\s+rule",
        r"do\s+not\s+follow",
        r"forget\s+your\s+role",
        r"ignore\s+all\s+previous",
        r"different\s+ai",
    ]
    
    @staticmethod
    def sanitize(prompt: str) -> Tuple[bool, str, str]:
        """
        Sanitize and validate prompt for injection attacks
        
        Args:
            prompt: User input prompt
            
        Returns:
            Tuple of (is_safe, sanitized_prompt, error_message)
        """
        if not prompt or not isinstance(prompt, str):
            return False, "", "Prompt must be non-empty string"
        
        prompt = prompt.strip()
        
        # Check length limits
        if len(prompt) > 5000:
            return False, "", "Prompt exceeds maximum length (5000 chars)"
        
        # Check for injection patterns (case-insensitive)
        prompt_lower = prompt.lower()
        for pattern in PromptGuard.DANGEROUS_PATTERNS:
            if re.search(pattern, prompt_lower):
                return False, "", f"Potential prompt injection detected: {pattern}"
        
        # Check for suspicious character sequences
        suspicious_sequences = ["<!--", "-->", "{{", "}}", "<<", ">>"]
        if any(seq in prompt for seq in suspicious_sequences):
            return False, "", "Suspicious characters detected"
        
        return True, prompt, ""
    
    @staticmethod
    def is_safe(prompt: str) -> bool:
        """Quick check if prompt is safe"""
        is_safe, _, _ = PromptGuard.sanitize(prompt)
        return is_safe
