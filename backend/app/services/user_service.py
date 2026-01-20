"""User service for proj3."""

from typing import List
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.core.exceptions import NotFoundError, ValidationError


class UserService:
    """Service for user business logic."""
    
    def __init__(self, db: Session):
        """Initialize user service.
        
        Args:
            db: Database session
        """
        self.repository = UserRepository(db)
    
    def get_user(self, user_id: int) -> UserRead:
        """Get a user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            UserRead with user data
            
        Raises:
            NotFoundError: If user not found
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return UserRead.model_validate(user)
    
    def list_users(self, skip: int = 0, limit: int = 100) -> tuple[List[UserRead], int]:
        """List users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (list of users, total count)
        """
        users = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return [UserRead.model_validate(user) for user in users], total
    
    def create_user(self, user_data: UserCreate) -> UserRead:
        """Create a new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            UserRead with created user data
            
        Raises:
            ValidationError: If email already exists
        """
        if self.repository.email_exists(user_data.email):
            raise ValidationError(f"User with email {user_data.email} already exists")
        
        user = self.repository.create(**user_data.model_dump())
        return UserRead.model_validate(user)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> UserRead:
        """Update a user.
        
        Args:
            user_id: User ID
            user_data: User update data
            
        Returns:
            UserRead with updated user data
            
        Raises:
            NotFoundError: If user not found
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        update_data = user_data.model_dump(exclude_unset=True)
        updated_user = self.repository.update(user, **update_data)
        return UserRead.model_validate(updated_user)
    
    def delete_user(self, user_id: int) -> None:
        """Delete a user.
        
        Args:
            user_id: User ID
            
        Raises:
            NotFoundError: If user not found
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        
        self.repository.delete(user)


