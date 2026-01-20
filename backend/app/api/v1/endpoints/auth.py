"""Authentication endpoints for proj3."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.db import get_seed_db
from app.services.auth_service import AuthService
from app.core.exceptions import NotFoundError

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr


class LoginResponse(BaseModel):
    """Login response schema."""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    display_name: str
    role: str
    run_id: str


def get_auth_service(db: Session = Depends(get_seed_db)) -> AuthService:
    """Dependency to get auth service."""
    return AuthService(db)


@router.post("/auth/token", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(
    login_data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Login endpoint that accepts email and returns JWT token.
    
    Args:
        login_data: Login request containing email
        service: Auth service instance
        
    Returns:
        LoginResponse with JWT access token, user info, and run_id
        
    Raises:
        HTTPException: If email not found in database
    """
    try:
        result = service.login(login_data.email)
        return LoginResponse(**result)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/auth/logout", status_code=status.HTTP_200_OK)
def logout(
    request: Request,
    service: AuthService = Depends(get_auth_service),
):
    """Logout endpoint that revokes the current token."""
    token_data = getattr(request.state, "token_data", None)
    if token_data:
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            return service.logout(token)
    
    return {"message": "Logged out successfully"}

