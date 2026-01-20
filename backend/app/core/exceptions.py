"""Custom exceptions for proj3."""

from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    """Base exception for application errors."""
    
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(BaseAppException):
    """Raised when a resource is not found."""
    
    def __init__(self, resource: str, identifier: str | int):
        detail = f"{resource} with identifier '{identifier}' not found"
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ValidationError(BaseAppException):
    """Raised when validation fails."""
    
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class UnauthorizedError(BaseAppException):
    """Raised when authentication is required but not provided."""
    
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(BaseAppException):
    """Raised when user doesn't have permission."""
    
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


