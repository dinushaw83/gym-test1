"""FastAPI dependencies for authentication in proj3."""

from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.auth.token_manager import TokenData, get_token_manager
from app.db import get_db
from app.models.user import User


def require_token_data(request: Request) -> TokenData:
    """Dependency: require valid token data from request."""
    token_data = getattr(request.state, "token_data", None)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return token_data


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    """Dependency: resolve current authenticated user (required)."""
    token_data = require_token_data(request)
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with token not found",
        )
    
    user._token_role = token_data.role
    return user


def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Dependency: resolve current user if token is present, else None."""
    token_data = getattr(request.state, "token_data", None)
    if not token_data:
        return None
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user:
        user._token_role = token_data.role
    return user


