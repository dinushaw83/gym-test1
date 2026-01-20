"""Base repository class for proj3."""

from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.db import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository providing common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        """Initialize repository.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def count(self) -> int:
        """Count total number of records.
        
        Returns:
            Total count
        """
        return self.db.query(self.model).count()
    
    def create(self, **kwargs) -> ModelType:
        """Create a new record.
        
        Args:
            **kwargs: Model attributes
            
        Returns:
            Created model instance
        """
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """Update an existing record.
        
        Args:
            instance: Model instance to update
            **kwargs: Attributes to update
            
        Returns:
            Updated model instance
        """
        for key, value in kwargs.items():
            setattr(instance, key, value)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def delete(self, instance: ModelType) -> None:
        """Delete a record.
        
        Args:
            instance: Model instance to delete
        """
        self.db.delete(instance)
        self.db.commit()


