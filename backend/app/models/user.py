"""User model for proj3."""

from typing import Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base
from app.models.mixins import TimestampMixin
from app.models.enums import UserRole


class User(Base, TimestampMixin):
    """User model representing application users."""
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.MEMBER, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', display_name='{self.display_name}')>"


