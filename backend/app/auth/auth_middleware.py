"""Authentication middleware for proj3."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.token_manager import get_token_manager


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate JWT tokens and set request state."""
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        public_paths = ["/health", "/docs", "/openapi.json", "/redoc"]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # Allow requests without auth (will fail later if endpoint requires it)
            return await call_next(request)
        
        token = auth_header.split(" ")[1]
        token_manager = get_token_manager()
        token_data = token_manager.validate_token(token)
        
        if token_data:
            request.state.token_data = token_data
            request.state.run_id = token_data.run_id
        else:
            # Invalid token - return 401
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"},
            )
        
        return await call_next(request)


def auth_middleware(app):
    """Add authentication middleware to FastAPI app."""
    app.add_middleware(AuthMiddleware)
    return app


