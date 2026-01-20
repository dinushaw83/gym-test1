"""User endpoints for proj3."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.user import UserCreate, UserUpdate, UserRead, UserListResponse
from app.services.user_service import UserService
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.auth.rbac import require_admin
from app.core.exceptions import NotFoundError, ValidationError

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to get user service."""
    return UserService(db)


@router.get("/users", response_model=UserListResponse)
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """List all users with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Authenticated user
        service: User service instance
        
    Returns:
        UserListResponse with list of users and total count
    """
    users, total = service.list_users(skip=skip, limit=limit)
    
    return UserListResponse(
        items=users,
        total=total,
    )


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Get a single user by ID.
    
    Args:
        user_id: User ID
        current_user: Authenticated user
        service: User service instance
        
    Returns:
        UserRead with user data
        
    Raises:
        HTTPException: 404 if user not found
    """
    try:
        return service.get_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_admin()),
    service: UserService = Depends(get_user_service),
):
    """Create a new user.
    
    Args:
        user_data: User creation data
        current_user: Authenticated user (must be admin)
        service: User service instance
        
    Returns:
        UserRead with created user data
        
    Raises:
        HTTPException: 400 if validation fails, 403 if not admin
    """
    try:
        return service.create_user(user_data)
    except ValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.patch("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Update a user.
    
    Args:
        user_id: User ID
        user_data: User update data
        current_user: Authenticated user
        service: User service instance
        
    Returns:
        UserRead with updated user data
        
    Raises:
        HTTPException: 404 if user not found, 403 if not authorized
    """
    # Only admins can update other users, or users can update themselves
    if current_user.id != user_id:
        if current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own profile"
            )
    
    try:
        return service.update_user(user_id, user_data)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin()),
    service: UserService = Depends(get_user_service),
):
    """Delete a user.
    
    Args:
        user_id: User ID
        current_user: Authenticated user (must be admin)
        service: User service instance
        
    Raises:
        HTTPException: 404 if user not found, 403 if not admin
    """
    try:
        service.delete_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    return None


