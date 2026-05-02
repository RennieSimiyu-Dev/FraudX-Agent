"""
Authentication module for FraudX Agent.
Handles user registration, login, password hashing, and JWT token management.
"""
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "fraudx-secret-key-change-in-production-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Path to analysts database
ANALYSTS_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "analysts.json")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
    
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token to decode
    
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def load_analysts_db() -> Dict[str, Any]:
    """
    Load analysts database from JSON file.
    
    Returns:
        Dictionary of analysts
    """
    if not os.path.exists(ANALYSTS_DB_PATH):
        return {}
    
    try:
        with open(ANALYSTS_DB_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def save_analysts_db(analysts: Dict[str, Any]) -> None:
    """
    Save analysts database to JSON file.
    
    Args:
        analysts: Dictionary of analysts to save
    """
    os.makedirs(os.path.dirname(ANALYSTS_DB_PATH), exist_ok=True)
    with open(ANALYSTS_DB_PATH, 'w') as f:
        json.dump(analysts, f, indent=2)


def get_analyst(analyst_id: str) -> Optional[Dict[str, Any]]:
    """
    Get analyst by ID from database.
    
    Args:
        analyst_id: Analyst identifier
    
    Returns:
        Analyst data or None if not found
    """
    analysts = load_analysts_db()
    return analysts.get(analyst_id)


def authenticate_analyst(analyst_id: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate an analyst with ID and password.
    
    Args:
        analyst_id: Analyst identifier
        password: Plain text password
    
    Returns:
        Analyst data (without password) if authenticated, None otherwise
    """
    analyst = get_analyst(analyst_id)
    if not analyst:
        return None
    
    if not verify_password(password, analyst["hashed_password"]):
        return None
    
    # Return analyst data without password
    analyst_data = analyst.copy()
    analyst_data.pop("hashed_password", None)
    return analyst_data


def validate_token(token: str) -> Dict[str, Any]:
    """
    Validate a JWT token and return the payload.
    
    Args:
        token: JWT token to validate
    
    Returns:
        Token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

# Made with Bob
