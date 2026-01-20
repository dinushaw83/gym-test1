"""User repository for proj3."""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""
    
    def __init__(self, db: Session):
        """Initialize user repository.
        
        Args:
            db: Database session
        """
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email.
        
        Args:
            email: User email address
            
        Returns:
            User instance or None if not found
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists.
        
        Args:
            email: Email address to check
            
        Returns:
            True if email exists, False otherwise
        """
        return self.get_by_email(email) is not None


