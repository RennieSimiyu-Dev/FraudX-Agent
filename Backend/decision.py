"""
Decision module for determining actions based on fraud risk scores.
"""
from typing import Literal


ActionType = Literal["APPROVE", "VERIFY_USER", "ANALYST_QUEUE"]


def decide(score: int) -> ActionType:
    """
    Determine the appropriate action based on fraud risk score.
    
    Score ranges:
    - 0-29: Low risk - Approve automatically
    - 30-69: Medium risk - Request user verification
    - 70-100: High risk - Send to analyst queue for manual review
    
    Args:
        score: Fraud risk score (0-100)
    
    Returns:
        Action to take: "APPROVE", "VERIFY_USER", or "ANALYST_QUEUE"
    
    Raises:
        ValueError: If score is not in valid range
    """
    if not isinstance(score, (int, float)):
        raise ValueError(f"Score must be a number, got {type(score)}")
    
    if not 0 <= score <= 100:
        raise ValueError(f"Score must be between 0 and 100, got {score}")
    
    if score < 30:
        return "APPROVE"
    elif score < 70:
        return "VERIFY_USER"
    else:
        return "ANALYST_QUEUE"


def get_risk_level(score: int) -> str:
    """
    Get human-readable risk level description.
    
    Args:
        score: Fraud risk score (0-100)
    
    Returns:
        Risk level: "Low", "Medium", or "High"
    """
    if score < 30:
        return "Low"
    elif score < 70:
        return "Medium"
    else:
        return "High"

# Made with Bob
