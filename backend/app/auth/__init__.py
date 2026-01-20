"""Authentication module for proj3."""

from app.auth.token_manager import TokenData, TokenManager, get_token_manager
from app.auth.dependencies import (
    get_current_user,
    get_current_user_optional,
    require_token_data,
)
from app.auth.rbac import (
    require_role,
    require_admin,
    require_member_or_admin,
    authorized,
)
from app.auth.auth_middleware import auth_middleware

__all__ = [
    "TokenData",
    "TokenManager",
    "get_token_manager",
    "get_current_user",
    "get_current_user_optional",
    "require_token_data",
    "require_role",
    "require_admin",
    "require_member_or_admin",
    "authorized",
    "auth_middleware",
]


