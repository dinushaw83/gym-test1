"""FastAPI application entrypoint for proj3 backend."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import (
    API_V1_PREFIX,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS,
)
from app.seed_manager import initialize_seed
from app.api.v1 import router as api_v1_router
from app.auth.auth_middleware import auth_middleware
from app.instrumentation import setup_instrumentation
from app.metrics_middleware import metrics_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup: Initialize instrumentation and seed database
    logger.info("Starting proj3 backend...")
    
    # Initialize OpenTelemetry instrumentation
    setup_instrumentation()
    
    try:
        initialize_seed()
        logger.info("✅ Seed database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize seed database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down proj3 backend...")


app = FastAPI(
    title="proj3 API",
    description="proj3 project management backend",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Add metrics middleware (before auth to track all requests)
metrics_middleware(app)

# Add authentication middleware
auth_middleware(app)

# Gym identification middleware
@app.middleware("http")
async def gym_middleware(request, call_next):
    request.state.gym_name = "proj3"
    return await call_next(request)


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "gym": "proj3",
        "version": "1.0.0"
    }


# Include API routers
app.include_router(api_v1_router, prefix=API_V1_PREFIX)


# Root endpoint
@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "proj3 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8880)
