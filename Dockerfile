# Multi-stage Dockerfile for abcd Gym
# Builds both frontend and backend in a single image
#
# NOTE: This combined container approach is suitable for development/testing.
# For production, consider separating into:
# - A dedicated backend container (Python/FastAPI)
# - A dedicated frontend container (Next.js)
# This allows independent scaling, updates, and better resource management.

# ============================================
# Stage 1: Build Frontend
# ============================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Install build dependencies for native modules
RUN apk add --no-cache python3 make g++

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps --no-audit

# Copy frontend code
COPY frontend/ .

# Build arguments
ARG NEXT_PUBLIC_API_BASE_PATH
ARG NEXT_PUBLIC_ENABLE_INSTRUMENTATION
ARG NEXT_PUBLIC_OTEL_ENDPOINT

ENV NEXT_PUBLIC_API_BASE_PATH=$NEXT_PUBLIC_API_BASE_PATH
ENV NEXT_PUBLIC_ENABLE_INSTRUMENTATION=$NEXT_PUBLIC_ENABLE_INSTRUMENTATION
ENV NEXT_PUBLIC_OTEL_ENDPOINT=$NEXT_PUBLIC_OTEL_ENDPOINT

# Build Next.js app
RUN npm run build

# ============================================
# Stage 2: Build Backend
# ============================================
FROM python:3.11-slim AS backend-builder

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend app code
COPY backend/app/ ./app/

# ============================================
# Stage 3: Runtime Image
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies including Node.js
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy backend from builder
COPY --from=backend-builder /app/backend ./backend
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy frontend from builder
COPY --from=frontend-builder /app/frontend/.next/standalone ./.next/standalone
COPY --from=frontend-builder /app/frontend/.next/static ./.next/static
COPY --from=frontend-builder /app/frontend/public ./public

# Create symlinks so standalone server can find static files and public assets
# Next.js standalone server expects .next/static and public relative to the standalone directory
RUN mkdir -p /app/.next/standalone/.next && \
    ln -s /app/.next/static /app/.next/standalone/.next/static && \
    ln -s /app/public /app/.next/standalone/public

# Copy verifiers and trajectories
COPY verifiers/ ./verifiers/
COPY trajectories/ ./trajectories/

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql+psycopg2://abcd:abcd@postgres:5432/postgres
ENV POSTGRES_TEMPLATE_DB=abcd_seed
ENV POSTGRES_RUN_DB_PREFIX=abcd_

# Expose ports
EXPOSE 5173 8880

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8880/health || exit 1

# Start both services
CMD ["sh", "-c", \
     "cd /app/backend && PYTHONPATH=/app/backend uvicorn app.main:app --host 0.0.0.0 --port 8880 & \
      cd /app/.next/standalone && PORT=5173 node server.js"]


