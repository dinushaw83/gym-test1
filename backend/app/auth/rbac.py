"""Role-based access control utilities for proj3."""

from typing import List, Optional
from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.enums import UserRole


def _normalize_role(role) -> str:
    """Normalize role to lowercase string."""
    if hasattr(role, "value"):
        return role.value.lower()
    return str(role).lower()


def require_role(allowed_roles: List[str]):
    """Dependency factory: require user to have one of the allowed roles."""
    def role_checker(current_user: User = Depends(get_current_user)) -> None:
        user_role = _normalize_role(
            getattr(current_user, "_token_role", None) or current_user.role
        )
        allowed = [_normalize_role(r) for r in allowed_roles]
        if user_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of these roles: {', '.join(allowed_roles)}",
            )
    return role_checker


def require_admin():
    """Dependency requiring admin role."""
    return require_role(["admin"])


def require_member_or_admin():
    """Dependency requiring member or admin role."""
    return require_role(["admin", "member"])


def authorized(allowed_roles: Optional[List[str]] = None):
    """FastAPI-style authorization dependency for endpoints.
    
    Usage:
        @router.get("/secure", dependencies=[Depends(authorized())])
        def secure_route():
            ...
            
        @router.get("/admin-only", dependencies=[Depends(authorized(["admin"]))])
        def admin_route():
            ...
    """
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if allowed_roles:
            user_role = _normalize_role(
                getattr(current_user, "_token_role", None) or current_user.role
            )
            allowed = [_normalize_role(r) for r in allowed_roles]
            if user_role not in allowed:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to perform this action.",
                )
        return current_user
    return dependency


