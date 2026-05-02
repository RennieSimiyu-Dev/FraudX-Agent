"""
User verification module for processing user responses to fraud alerts.
"""
from typing import Literal


VerificationResult = Literal["APPROVED_BY_USER", "BLOCKED", "INVALID_RESPONSE"]


def verify_user(response: str) -> VerificationResult:
    """
    Process user's verification response to determine transaction approval.
    
    Args:
        response: User's response to verification request
    
    Returns:
        Verification result:
        - "APPROVED_BY_USER": User confirmed the transaction
        - "BLOCKED": User denied the transaction
        - "INVALID_RESPONSE": Response was not recognized
    """
    if not isinstance(response, str):
        return "INVALID_RESPONSE"
    
    response_lower = response.strip().lower()
    
    # Positive responses
    positive_responses = {"yes", "y", "approve", "approved", "confirm", "confirmed", "ok", "okay"}
    if response_lower in positive_responses:
        return "APPROVED_BY_USER"
    
    # Negative responses
    negative_responses = {"no", "n", "deny", "denied", "block", "blocked", "reject", "rejected"}
    if response_lower in negative_responses:
        return "BLOCKED"
    
    # Unrecognized response
    return "INVALID_RESPONSE"


def is_valid_response(response: str) -> bool:
    """
    Check if a response is valid (recognized).
    
    Args:
        response: User's response
    
    Returns:
        True if response is recognized, False otherwise
    """
    return verify_user(response) != "INVALID_RESPONSE"

# Made with Bob
