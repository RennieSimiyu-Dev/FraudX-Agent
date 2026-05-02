"""
Fraud detection agent module.
Analyzes transactions and calculates fraud risk scores.
"""
from typing import Dict, List, Tuple, Any


def fraud_agent(txn: Dict[str, Any], profile: Dict[str, Any]) -> Tuple[int, List[str]]:
    """
    Calculate fraud risk score for a transaction based on user profile.
    
    Args:
        txn: Transaction data containing:
            - amount (float): Transaction amount
            - country (str): Country code
            - device (str): Device identifier
            - merchant (str, optional): Merchant identifier
        profile: User profile containing:
            - avg_amount (float): Average transaction amount
            - countries (List[str]): Known countries
            - devices (List[str]): Known devices
            - merchants (List[str], optional): Known merchants
    
    Returns:
        Tuple containing:
            - score (int): Fraud risk score (0-100)
            - reasons (List[str]): List of risk factors identified
    
    Raises:
        ValueError: If required fields are missing
    """
    # Validate required fields
    required_txn_fields = ["amount", "country", "device"]
    required_profile_fields = ["avg_amount", "countries", "devices"]
    
    for field in required_txn_fields:
        if field not in txn:
            raise ValueError(f"Missing required transaction field: {field}")
    
    for field in required_profile_fields:
        if field not in profile:
            raise ValueError(f"Missing required profile field: {field}")
    
    score = 0
    reasons = []
    
    # Extract transaction data
    amount = float(txn["amount"])
    country = txn["country"]
    device = txn["device"]
    merchant = txn.get("merchant")
    
    # Extract profile data
    avg_amount = float(profile["avg_amount"])
    known_countries = profile["countries"]
    known_devices = profile["devices"]
    known_merchants = profile.get("merchants", [])
    
    # Check for unusual amount
    if avg_amount > 0:
        if amount >= avg_amount * 5:
            score += 40
            reasons.append(f"Extremely high amount: ${amount:.2f} vs avg ${avg_amount:.2f}")
        elif amount >= avg_amount * 3:
            score += 30
            reasons.append(f"Very high amount: ${amount:.2f} vs avg ${avg_amount:.2f}")
        elif amount >= avg_amount * 2:
            score += 20
            reasons.append(f"High amount: ${amount:.2f} vs avg ${avg_amount:.2f}")
    
    # Check for new country
    if country not in known_countries:
        score += 25
        reasons.append(f"New country detected: {country}")
    
    # Check for unknown device
    if device not in known_devices:
        score += 20
        reasons.append(f"Unknown device: {device}")
    
    # Check for new merchant (if provided)
    if merchant and merchant not in known_merchants:
        score += 15
        reasons.append(f"New merchant: {merchant}")
    
    # Cap score at 100
    score = min(score, 100)
    
    return score, reasons

# Made with Bob
