"""Database router for run_id-based database isolation for proj3."""

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy.engine import make_url
from threading import Lock
from typing import Dict, Optional
import logging

from app.config import (
    DATABASE_URL,
    POSTGRES_ADMIN_DB,
    POSTGRES_TEMPLATE_DB,
    POSTGRES_RUN_DB_PREFIX,
)

logger = logging.getLogger(__name__)
_db_creation_lock = Lock()

# Cache of per-run engines
_run_engines: Dict[str, any] = {}
_engine_lock = Lock()


def get_run_db_name(run_id: str) -> str:
    """Get the database name for a given run_id."""
    return f"{POSTGRES_RUN_DB_PREFIX}{run_id}"


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


def _clone_postgres_database(template_db: str, new_db: str):
    """Clone a Postgres database from a template."""
    engine = _postgres_admin_engine()
    try:
        with engine.connect() as conn:
            # Terminate existing connections to template
            conn.execute(text(f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = '{template_db}' AND pid <> pg_backend_pid()
            """))
            # Create new database from template
            conn.execute(text(f'CREATE DATABASE "{new_db}" TEMPLATE "{template_db}"'))
            logger.info(f"Cloned database {new_db} from template {template_db}")
    finally:
        engine.dispose()


def ensure_run_database(run_id: str):
    """Ensure the run database exists, creating it if necessary."""
    db_name = get_run_db_name(run_id)
    
    if _postgres_database_exists(db_name):
        return
    
    with _db_creation_lock:
        # Double-check after acquiring lock
        if _postgres_database_exists(db_name):
            return
        
        if not _postgres_database_exists(POSTGRES_TEMPLATE_DB):
            raise RuntimeError(
                f"Template database {POSTGRES_TEMPLATE_DB} does not exist. "
                "Please run initialization scripts first."
            )
        
        _clone_postgres_database(POSTGRES_TEMPLATE_DB, db_name)


def get_engine(run_id: str):
    """Get or create SQLAlchemy engine for a run_id."""
    with _engine_lock:
        if run_id in _run_engines:
            return _run_engines[run_id]
    
    ensure_run_database(run_id)
    db_name = get_run_db_name(run_id)
    url = make_url(DATABASE_URL).set(database=db_name)
    
    engine = create_engine(
        url,
        pool_pre_ping=True,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=15,
    )
    
    with _engine_lock:
        _run_engines[run_id] = engine
    
    return engine


