"""Postgres template database management for proj3."""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool

from app.config import DATABASE_URL, POSTGRES_ADMIN_DB, POSTGRES_TEMPLATE_DB

logger = logging.getLogger(__name__)


def _postgres_admin_engine():
    """Create an admin engine for Postgres."""
    url = make_url(DATABASE_URL).set(database=POSTGRES_ADMIN_DB)
    return create_engine(
        url, isolation_level="AUTOCOMMIT", pool_pre_ping=True, poolclass=NullPool
    )


def _postgres_database_exists(db_name: str) -> bool:
    """Check if a Postgres database exists."""
    engine = _postgres_admin_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname=:name"),
                {"name": db_name},
            ).scalar()
            return result is not None
    finally:
        engine.dispose()


def _postgres_ensure_template_database():
    """Ensure the Postgres template database exists."""
    if _postgres_database_exists(POSTGRES_TEMPLATE_DB):
        # Database exists, ensure tables are created
        _ensure_template_tables()
        return

    engine = _postgres_admin_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE {POSTGRES_TEMPLATE_DB}"))
            logger.info(f"Created Postgres template database: {POSTGRES_TEMPLATE_DB}")
    finally:
        engine.dispose()
    
    # Create tables in the template database
    _ensure_template_tables()


def _ensure_template_tables():
    """Ensure all tables exist in the template database."""
    # Import here to avoid circular import with app.db
    # Note: User model uses app.db.Base, so we must import from app.db, not app.database
    from app.db import Base
    from app.models import User  # Import all models to register them with Base
    
    template_url = make_url(DATABASE_URL).set(database=POSTGRES_TEMPLATE_DB)
    engine = create_engine(
        template_url, isolation_level="AUTOCOMMIT", pool_pre_ping=True, poolclass=NullPool
    )
    try:
        # Check existing tables
        with engine.connect() as conn:
            existing_tables = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
            """)).fetchall()
            existing_table_names = [row[0] for row in existing_tables]
            logger.info(f"Existing tables in {POSTGRES_TEMPLATE_DB}: {existing_table_names}")
        
        # Create all tables defined in models
        logger.info(f"Creating tables in template database: {POSTGRES_TEMPLATE_DB}")
        logger.info(f"Registered tables in Base.metadata: {list(Base.metadata.tables.keys())}")
        if not Base.metadata.tables:
            raise RuntimeError(
                "No tables registered in Base.metadata. "
                "Make sure all models are imported before calling create_all()."
            )
        Base.metadata.create_all(engine)
        
        # Verify tables were created
        with engine.connect() as conn:
            created_tables = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
            """)).fetchall()
            created_table_names = [row[0] for row in created_tables]
            logger.info(f"Tables in {POSTGRES_TEMPLATE_DB} after creation: {created_table_names}")
            
            if not created_table_names:
                raise RuntimeError(
                    f"No tables found in template database {POSTGRES_TEMPLATE_DB}. "
                    "Table creation may have failed."
                )
        
        logger.info(f"✅ Successfully ensured tables exist in template database: {POSTGRES_TEMPLATE_DB}")
    except Exception as e:
        logger.error(f"❌ Failed to create tables in template database {POSTGRES_TEMPLATE_DB}: {e}")
        raise
    finally:
        engine.dispose()


def initialize_seed():
    """Ensure the Postgres template database exists (idempotent)."""
    _postgres_ensure_template_database()


