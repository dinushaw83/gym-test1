"""Authentication service for proj3."""

import uuid
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.auth.token_manager import get_token_manager
from app.db_router import ensure_run_database
from app.core.exceptions import NotFoundError


class AuthService:
    """Service for authentication business logic."""
    
    def __init__(self, db: Session):
        """Initialize auth service.
        
        Args:
            db: Database session (seed database)
        """
        self.repository = UserRepository(db)
    
    def login(self, email: str) -> dict:
        """Login user and generate token.
        
        Args:
            email: User email address
            
        Returns:
            Dictionary with token and user information
            
        Raises:
            NotFoundError: If user not found
        """
        user = self.repository.get_by_email(email)
        if not user:
            raise NotFoundError("User", email)
        
        # Generate unique run_id for this login session
        run_id = str(uuid.uuid4())
        
        # Initialize run database by cloning from template
        ensure_run_database(run_id)
        
        # Get user role
        role = user.role.value if hasattr(user.role, "value") else str(user.role)
        
        # Generate JWT token
        token_manager = get_token_manager()
        access_token = token_manager.create_token(
            user_id=user.id,
            role=role,
            email=user.email,
            run_id=run_id,
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
            "display_name": user.display_name,
            "role": role,
            "run_id": run_id,
        }
    
    def logout(self, token: str) -> dict:
        """Logout user by revoking token.
        
        Args:
            token: JWT token to revoke
            
        Returns:
            Success message
        """
        token_manager = get_token_manager()
        token_manager.revoke_token(token)
        return {"message": "Logged out successfully"}


