"""Database connection setup and session management for proj3."""

from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.engine import make_url
from app.db_router import get_engine
from app.seed_manager import initialize_seed
from app.config import DATABASE_URL, POSTGRES_TEMPLATE_DB

# Base class for all SQLAlchemy models
Base = declarative_base()

# Seed database engine and session (used by initialization scripts)
_seed_engine = None


def _get_seed_engine():
    """Get or create a SQLAlchemy engine for the seed database."""
    global _seed_engine
    if _seed_engine is None:
        initialize_seed()
        template_url = make_url(DATABASE_URL).set(database=POSTGRES_TEMPLATE_DB)
        _seed_engine = create_engine(template_url, pool_pre_ping=True, poolclass=NullPool)
    return _seed_engine


def get_db(request: Request):
    """FastAPI dependency that provides a database session.
    
    Creates a session for the run-specific database based on run_id
    extracted from the request state by middleware.
    
    Args:
        request: FastAPI request object with run_id in state.
        
    Yields:
        Database session instance for the run-specific database.
    """
    if not hasattr(request.state, 'run_id') or not request.state.run_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token."
        )
    
    run_id = request.state.run_id
    engine = get_engine(run_id)
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_seed_db():
    """FastAPI dependency that provides a database session to the seed/template database."""
    engine = _get_seed_engine()
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


