"""Application configuration constants for proj3 backend."""

import os
from pathlib import Path

# Base directory for the backend application
BASE_DIR = Path(__file__).resolve().parent.parent

# Project root (parent of backend directory)
PROJECT_ROOT = BASE_DIR.parent

# Database connection URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://proj3:proj3@127.0.0.1:5431/postgres",
)

# Postgres template cloning settings
POSTGRES_ADMIN_DB = os.getenv("POSTGRES_ADMIN_DB", "postgres")
POSTGRES_TEMPLATE_DB = os.getenv("POSTGRES_TEMPLATE_DB", "proj3_seed")
POSTGRES_RUN_DB_PREFIX = os.getenv("POSTGRES_RUN_DB_PREFIX", "proj3_")

# Cleanup Settings
CLEANUP_TIMEOUT_HOURS = 24
CLEANUP_INTERVAL_SECONDS = 3600  # 1 hour

# API Configuration
API_V1_PREFIX = "/api/v1"

# CORS Configuration
ALLOW_ALL_ORIGINS = os.getenv("ALLOW_ALL_ORIGINS", "true").lower() == "true"

if ALLOW_ALL_ORIGINS:
    CORS_ORIGINS = ["*"]
else:
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    if FRONTEND_URL:
        CORS_ORIGINS.append(FRONTEND_URL)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# JWT Authentication Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-production-please")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ISSUER = os.getenv("JWT_ISSUER", "proj3")
JWT_ACCESS_TOKEN_TTL_SECONDS = int(os.getenv("JWT_ACCESS_TOKEN_TTL_SECONDS", "86400"))  # 24 hours


