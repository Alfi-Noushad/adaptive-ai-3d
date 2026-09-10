from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
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

router = APIRouter(prefix="/auth", tags=["Authentication"])

fake_users_db = {}

def make_envelope(message: str, data=None, error=None, status_code="ok"):
    return {
        "status": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@router.post("/register")
def register(user_data: UserRegisterRequest):
    if user_data.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = get_password_hash(user_data.password)
    fake_users_db[user_data.email] = {
        "email": user_data.email,
        "username": user_data.username or user_data.email.split("@")[0],
        "password_hash": hashed,
        "role": user_data.role,
    }
    
    return make_envelope(
        message="User registered successfully",
        data={"email": user_data.email, "role": user_data.role},
    )

@router.post("/login")
def login(credentials: UserLoginRequest):
    user = fake_users_db.get(credentials.email)
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    payload = {"sub": user["email"], "role": user["role"]}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    
    return make_envelope(
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "email": user["email"],
            "role": user["role"],
        },
    )

@router.post("/refresh")
def refresh_token(request: TokenRefreshRequest):
    payload = decode_token(request.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type, refresh token required",
        )
    
    email = payload.get("sub")
    role = payload.get("role", "user")
    new_access_token = create_access_token({"sub": email, "role": role})
    
    return make_envelope(
        message="Token refreshed successfully",
        data={
            "access_token": new_access_token,
            "token_type": "bearer",
        },
    )

@router.post("/logout")
def logout(current_user: Annotated[dict, Depends(get_current_user)]):
    return make_envelope(
        message="User logged out successfully. Discard stored tokens on client.",
        data={"email": current_user["email"]},
    )

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    return make_envelope(
        message="If this email exists in our records, a password reset link has been dispatched.",
        data={"email": request.email},
    )

# Protected route sample demonstrating Depends() and RBAC
@router.get("/me")
def get_current_user_profile(current_user: Annotated[dict, Depends(get_current_user)]):
    return make_envelope(
        message="Profile retrieved successfully",
        data=current_user,
    )

@router.get("/admin-only")
def admin_only_endpoint(admin_user: Annotated[dict, Depends(require_role("admin"))]):
    return make_envelope(
        message="Admin access granted",
        data=admin_user,
    )