from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.entities import User
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenRefreshRequest,
    ForgotPasswordRequest,
)
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    require_role,
)
from app.core.response import api_response

router = APIRouter(prefix="/auth", tags=["Authentication"])

fake_users_db = {}

def make_envelope(message: str, data=None, error=None, status_code="success"):
    return {
        "status": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@router.post("/register")
def register(user_data: UserRegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed,
        role=user_data.role or "user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return api_response(
        status="success",
        message="User registered successfully",
        data={"id": new_user.id, "email": new_user.email, "role": new_user.role}
    )

@router.post("/login")
def login(credentials: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    payload = {"sub": user.email, "role": user.role, "user_id": user.id}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return api_response(
        status="success",
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "email": user.email,
            "role": user.role
        }
    )

@router.post("/refresh")
def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type, refresh token required"
        )
    
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_access_token = create_access_token({"sub": user.email, "role": user.role, "user_id": user.id})
    return api_response(
        status="success",
        message="Token refreshed successfully",
        data={
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    )

@router.post("/logout")
def logout(current_user: Annotated[dict, Depends(get_current_user)]):
    return api_response(
        status="success",
        message="User logged out successfully. Discard stored tokens on client.",
        data={"email": current_user.get("email")}
    )

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return api_response(
        status="success",
        message="If this email exists in our records, a password reset link has been dispatched.",
        data={"email": request.email}
    )

@router.get("/me")
def get_current_user_profile(current_user: Annotated[dict, Depends(get_current_user)]):
    return api_response(
        status="success",
        message="Profile retrieved successfully",
        data=current_user
    )

@router.get("/admin-only")
def admin_only_endpoint(admin_user: Annotated[dict, Depends(require_role("admin"))]):
    return api_response(
        status="success",
        message="Admin access granted",
        data=admin_user
    )
