from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from typing import Optional
from database.session import get_session
from models.user import User
from auth.jwt import verify_token
from auth.middleware import JWTBearer
from pydantic import BaseModel
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta, timezone
from core.config import settings

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user: dict
    token: str

@router.post("/api/auth/sign-up")
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,  # Changed to 409 Conflict
            detail="Email address already registered. Please use a different email or try logging in."
        )

    # Hash the password
    salt = secrets.token_hex(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', user_data.password.encode('utf-8'), bytes.fromhex(salt), 100000)
    hashed_password_hex = hashed_password.hex()

    # Create new user
    # Extract username from email (before @ symbol) to avoid NOT NULL constraint
    username = user_data.email.split('@')[0]
    db_user = User(
        email=user_data.email,
        username=username,
        hashed_password=f"{hashed_password_hex}:{salt}",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Check if BETTER_AUTH_SECRET is configured
    if not settings.BETTER_AUTH_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="BETTER_AUTH_SECRET environment variable is not configured"
        )

    # Create JWT token
    token_data = {
        "userId": str(db_user.id),  # Match the format expected by task endpoints
        "email": db_user.email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm="HS256")

    return {
        "user": {
            "id": str(db_user.id),
            "email": db_user.email
        },
        "token": token
    }


@router.post("/api/auth/sign-in/credentials")
def login_user(login_data: UserLogin, session: Session = Depends(get_session)):
    """
    Login user with credentials
    """
    # Find user by email
    db_user = session.exec(select(User).where(User.email == login_data.email)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password
    stored_hash, salt = db_user.hashed_password.split(':')
    computed_hash = hashlib.pbkdf2_hmac('sha256', login_data.password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()

    if stored_hash != computed_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Check if BETTER_AUTH_SECRET is configured
    if not settings.BETTER_AUTH_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="BETTER_AUTH_SECRET environment variable is not configured"
        )

    # Create JWT token
    token_data = {
        "userId": str(db_user.id),  # Match the format expected by task endpoints
        "email": db_user.email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm="HS256")

    return {
        "user": {
            "id": str(db_user.id),
            "email": db_user.email
        },
        "token": token
    }


@router.post("/api/auth/sign-out")
def logout_user(token_data: dict = Depends(JWTBearer())):
    """
    Logout user (in a real app, this might invalidate the token)
    """
    # In a real app, you might add the token to a blacklist
    return {"success": True}


# Health check for auth endpoints
@router.get("/api/auth/health")
def auth_health_check():
    return {"status": "healthy", "service": "Auth API"}