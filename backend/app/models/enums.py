"""Enums for proj3 models."""

from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


