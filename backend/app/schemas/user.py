"""User schemas for proj3."""

from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.enums import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    display_name: str
    avatar_url: Optional[str] = None
    role: UserRole = UserRole.MEMBER


class UserCreate(UserBase):
    """Schema for creating a user."""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[UserRole] = None


class UserRead(UserBase):
    """Schema for reading a user."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for user list response."""
    items: list[UserRead]
    total: int


