"""
FastAPI backend for fraud detection system.
Provides endpoints for transaction processing and user verification.
"""
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator, EmailStr

from agent import fraud_agent
from decision import decide
from analyst_queue import push_to_queue, get_queue
from verification import verify_user
from auth import (
    authenticate_analyst,
    create_access_token,
    validate_token
)

# Security
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login request model."""
    analyst_id: str = Field(..., min_length=3, description="Analyst identifier")
    password: str = Field(..., min_length=6, description="Password")


class AuthResponse(BaseModel):
    """Authentication response model."""
    access_token: str
    token_type: str = "bearer"
    analyst_id: str
    full_name: str
    email: str
    review_desk: str


def get_current_analyst(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency to get current authenticated analyst from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials
    
    Returns:
        Analyst data from token
    
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    payload = validate_token(token)
    return payload



app = FastAPI(
    title="FraudX Agent API",
    description="Fraud detection and transaction monitoring system",
    version="1.0.0"
)


class Transaction(BaseModel):
    """Transaction data model."""
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    country: str = Field(..., min_length=2, max_length=2, description="ISO country code")
    device: str = Field(..., min_length=1, description="Device identifier")
    merchant: str | None = Field(None, description="Merchant identifier")
    
    @validator('country')
    def country_uppercase(cls, v):
        return v.upper()


class UserProfile(BaseModel):
    """User profile data model."""
    avg_amount: float = Field(..., ge=0, description="Average transaction amount")
    countries: list[str] = Field(..., min_items=1, description="Known countries")
    devices: list[str] = Field(..., min_items=1, description="Known devices")
    merchants: list[str] = Field(default_factory=list, description="Known merchants")
    
    @validator('countries', each_item=True)
    def countries_uppercase(cls, v):
        return v.upper()


class TransactionRequest(BaseModel):
    """Request model for transaction processing."""
    transaction: Transaction
    profile: UserProfile


class VerificationRequest(BaseModel):
    """Request model for user verification."""
    response: str = Field(..., description="User's verification response")


class TransactionResponse(BaseModel):
    """Response model for transaction processing."""
    score: int
    reasons: list[str]
    action: str


class VerificationResponse(BaseModel):
    """Response model for verification."""
    verification_result: str




@app.post(
    "/auth/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"]
)
async def login(request: LoginRequest):
    """
    Authenticate an analyst and return access token.
    
    Args:
        request: Login credentials
    
    Returns:
        AuthResponse with access token and analyst data
    
    Raises:
        HTTPException: If credentials are invalid
    """
    analyst = authenticate_analyst(request.analyst_id, request.password)
    
    if not analyst:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid analyst ID or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": analyst["analyst_id"],
            "analyst_id": analyst["analyst_id"],
            "full_name": analyst["full_name"],
            "email": analyst["email"],
            "review_desk": analyst["review_desk"]
        }
    )
    
    return AuthResponse(
        access_token=access_token,
        analyst_id=analyst["analyst_id"],
        full_name=analyst["full_name"],
        email=analyst["email"],
        review_desk=analyst["review_desk"]
    )



@app.get(
    "/auth/me",
    tags=["Authentication"]
)
async def get_current_user(analyst: Dict[str, Any] = Depends(get_current_analyst)):
    """
    Get current authenticated analyst information.
    
    Args:
        analyst: Current analyst from token (injected by dependency)
    
    Returns:
        Current analyst data
    """
    return analyst

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "FraudX Agent API",
        "version": "1.0.0"
    }


@app.post(
    "/transaction",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Fraud Detection"]
)
async def process_transaction(request: TransactionRequest):
    """
    Process a transaction and calculate fraud risk score.
    
    Args:
        request: Transaction and user profile data
    
    Returns:
        TransactionResponse with score, reasons, and recommended action
    
    Raises:
        HTTPException: If processing fails
    """
    try:
        # Convert Pydantic models to dicts
        txn = request.transaction.dict()
        profile = request.profile.dict()
        
        # Calculate fraud score
        score, reasons = fraud_agent(txn, profile)
        
        # Determine action
        action = decide(score)
        
        # If flagged for analyst review, add to queue
        if action == "ANALYST_QUEUE":
            push_to_queue(txn, score, reasons)
        
        return TransactionResponse(
            score=score,
            reasons=reasons,
            action=action
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing error: {str(e)}"
        )


@app.post(
    "/verify",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Verification"]
)
async def verify_transaction(request: VerificationRequest):
    """
    Verify a transaction based on user response.
    
    Args:
        request: User's verification response
    
    Returns:
        VerificationResponse with verification result
    """
    try:
        result = verify_user(request.response)
        return VerificationResponse(verification_result=result)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification error: {str(e)}"
        )


@app.get(
    "/queue",
    tags=["Analyst Queue"]
)
async def get_analyst_queue():
    """
    Get all transactions in the analyst review queue.
    
    Returns:
        List of transactions awaiting analyst review
    """
    try:
        return {"queue": get_queue()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Queue retrieval error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

# Made with Bob
