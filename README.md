# Gym: proj3

> **UI Gym Project for LLM Training**

This is a standalone UI Gym project for LLM training. Each gym is delivered as a **single Docker image** containing both frontend and backend.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture](#architecture)
3. [Development Standards](#development-standards)
4. [Testing & Coverage](#testing--coverage)
5. [Project Structure](#project-structure)
6. [API Documentation](#api-documentation)
7. [Authentication & Authorization](#authentication--authorization)
8. [Database](#database)
9. [Docker & Deployment](#docker--deployment)
10. [Cursor Standards](#cursor-standards)
11. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (for containerized development)
- **Node.js 20+** (for local frontend development)
- **Python 3.11+** (for local backend development)
- **PostgreSQL 16+** (or use Docker)

### 1. Initial Setup

```bash
# Run automated setup script
./setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies (backend & frontend)
- Create necessary directories
- Set up environment variables

### 2. Start Development

**Option A: Docker (Recommended)**
```bash
docker-compose up -d
```

**Option B: Local Development**
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8880

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 3. Verify Installation

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8880
- **API Docs**: http://localhost:8880/docs
- **Health Check**: http://localhost:8880/health

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│  - React Components                                      │
│  - State Management                                      │
│  - API Client                                            │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│              Backend (FastAPI)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Auth API   │  │  Business    │  │   Database   │  │
│  │   (JWT)      │  │   Logic      │  │   Router     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              PostgreSQL Database                         │
│  - Seed Database (Template)                              │
│  - Run Databases (Per-run isolation)                     │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

1. **Run-ID Isolation**: Each user session gets an isolated database cloned from a template
2. **JWT Authentication**: Stateless authentication using JWT tokens
3. **Role-Based Access Control**: Admin, Member, Viewer roles with granular permissions
4. **API Versioning**: All endpoints under `/api/v1/`
5. **Docker-First**: Single Docker image contains both frontend and backend

### Technology Stack

**Backend:**
- FastAPI 0.115+ (Python web framework)
- SQLAlchemy 2.0+ (ORM)
- PostgreSQL 16+ (Database)
- Pydantic 2.10+ (Validation)
- PyJWT (Authentication)

**Frontend:**
- Next.js 16+ (React framework)
- TypeScript (Type safety)
- React Query (Data fetching)
- Tailwind CSS (Styling)

---

## 📐 Development Standards

### Code Style

#### Python (Backend)
- **Style Guide**: PEP 8
- **Line Length**: Maximum 100 characters
- **Type Hints**: Required for all function parameters and return types
- **Docstrings**: Google-style docstrings for all public functions/classes
- **Imports**: Use absolute imports, group by standard library, third-party, local

```python
# Good example - API Endpoint (Presentation Layer)
from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService
from app.schemas.user import UserRead
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserRead:
    """Get a user by ID.
    
    Args:
        user_id: User ID to retrieve
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
```

**Layered Architecture Flow:**
- **API Layer** (`api/v1/endpoints/`) → Handles HTTP requests/responses
- **Service Layer** (`services/`) → Contains business logic
- **Repository Layer** (`repositories/`) → Handles data access
- **Models** (`models/`) → SQLAlchemy ORM models

#### TypeScript (Frontend)
- **Style Guide**: ESLint + Prettier
- **Type Safety**: Strict mode enabled
- **Components**: Functional components with hooks
- **Exports**: Prefer named exports over default exports
- **Line Length**: Maximum 100 characters

```typescript
// Good example
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import type { User, UserListResponse } from '@/types/user';

export function useUsers(skip = 0, limit = 100) {
  return useQuery<UserListResponse>({
    queryKey: ['users', skip, limit],
    queryFn: () => apiClient.get('/api/v1/users', { params: { skip, limit } }),
  });
}
```

### File Organization

**Backend Structure (Layered Architecture):**
```
backend/app/
├── api/v1/              # API Layer (Presentation)
│   ├── endpoints/        # API endpoints (grouped by resource)
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── users.py       # User endpoints
│   │   └── ...
│   └── __init__.py       # Router aggregation
├── services/             # Business Logic Layer
│   ├── user_service.py   # User business logic
│   ├── auth_service.py   # Authentication logic
│   └── ...
├── repositories/         # Data Access Layer
│   ├── base.py           # Base repository
│   ├── user_repository.py # User data access
│   └── ...
├── models/               # SQLAlchemy ORM models
│   ├── user.py
│   ├── enums.py
│   └── ...
├── schemas/              # Pydantic validation schemas
│   ├── user.py
│   └── ...
├── core/                 # Core Infrastructure
│   ├── exceptions.py     # Custom exceptions
│   ├── security.py       # Security utilities
│   └── ...
├── db/                   # Database Layer
│   ├── session.py        # Database session management
│   └── ...
├── auth/                 # Authentication & Authorization
│   ├── token_manager.py
│   ├── dependencies.py
│   ├── rbac.py
│   └── auth_middleware.py
├── utils/                # Utility Functions
│   └── ...
├── db_router.py          # Run_id-based database routing
├── seed_manager.py       # Template database management
├── config.py             # Configuration settings
└── main.py               # FastAPI app entry point
```

**Frontend Structure:**
```
frontend/
├── app/             # Next.js app directory
│   ├── api/        # API routes (if needed)
│   └── ...
├── components/      # React components
│   ├── ui/         # UI components
│   └── ...
├── hooks/          # Custom React hooks
├── lib/            # Utility functions
│   ├── api-client.ts
│   └── ...
└── types/          # TypeScript type definitions
```

### Naming Conventions

- **Files**: `snake_case.py` (Python), `camelCase.ts` (TypeScript)
- **Classes**: `PascalCase`
- **Functions/Variables**: `snake_case` (Python), `camelCase` (TypeScript)
- **Constants**: `UPPER_SNAKE_CASE`
- **API Endpoints**: `kebab-case` (e.g., `/api/v1/user-roles`)

### Error Handling

**Backend:**
```python
from fastapi import HTTPException, status

# Always use proper HTTP status codes
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# Log errors appropriately
import logging
logger = logging.getLogger(__name__)
logger.error(f"Failed to process request: {error}", exc_info=True)
```

**Frontend:**
```typescript
try {
  const data = await apiClient.get('/api/v1/users');
} catch (error) {
  if (error instanceof APIError) {
    // Handle API error with user-friendly message
    toast.error(error.message);
  } else {
    // Handle unexpected error
    toast.error('An unexpected error occurred');
    console.error(error);
  }
}
```

### Security Best Practices

1. **Never commit secrets**: Use environment variables
2. **Validate all inputs**: Use Pydantic schemas (backend), Zod (frontend)
3. **Use parameterized queries**: SQLAlchemy handles this automatically
4. **Sanitize user input**: Before rendering in frontend
5. **HTTPS in production**: Always use HTTPS
6. **Rate limiting**: Implement for API endpoints
7. **CORS configuration**: Restrict in production

---

## 🧪 Testing & Coverage

### Test Coverage Requirements

- **Minimum Coverage**: **80%** for all new code
- **Critical Paths**: **100%** coverage required
- **Business Logic**: All functions must have tests
- **API Endpoints**: All endpoints must have integration tests

### Backend Testing

**Test Structure:**
```
backend/tests/
├── conftest.py           # Pytest fixtures
├── test_auth.py          # Authentication tests
├── test_rbac.py          # Authorization tests
├── test_api_users.py     # User API tests
└── test_integration.py   # Integration tests
```

**Running Tests:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api_users.py

# Run specific test
pytest tests/test_api_users.py::test_create_user

# Run with verbose output
pytest -v

# Run with coverage threshold (fail if below 80%)
pytest --cov=app --cov-fail-under=80
```

**Test Example:**
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user_success(client_with_auth):
    """Test successful user retrieval."""
    response = client_with_auth.get("/api/v1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "display_name" in data

def test_get_user_not_found(client_with_auth):
    """Test user not found error."""
    response = client_with_auth.get("/api/v1/users/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

### Frontend Testing

**Test Structure:**
```
frontend/
├── __tests__/
│   ├── components/
│   └── hooks/
└── ...
```

**Running Tests:**
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific test file
npm test -- UserList.test.tsx
```

**Test Example:**
```typescript
import { render, screen } from '@testing-library/react';
import { UserList } from '@/components/UserList';

describe('UserList', () => {
  it('renders user list correctly', () => {
    const users = [
      { id: 1, email: 'user1@example.com', display_name: 'User 1' },
      { id: 2, email: 'user2@example.com', display_name: 'User 2' },
    ];
    
    render(<UserList users={users} />);
    
    expect(screen.getByText('User 1')).toBeInTheDocument();
    expect(screen.getByText('User 2')).toBeInTheDocument();
  });
});
```

### Coverage Reports

- **Backend**: HTML report generated in `backend/htmlcov/`
- **Frontend**: Coverage report in `frontend/coverage/`
- **CI/CD**: Coverage reports must pass minimum threshold

---

## 📁 Project Structure

```
gym-proj3/
├── frontend/                  # Next.js frontend
│   ├── app/                  # App directory
│   ├── components/           # React components
│   ├── hooks/               # Custom hooks
│   ├── lib/                 # Utilities
│   ├── types/               # TypeScript types
│   ├── package.json
│   └── ...
│
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/v1/endpoints/ # API endpoints (Presentation Layer)
│   │   ├── services/         # Business Logic Layer
│   │   ├── repositories/     # Data Access Layer
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── core/             # Core infrastructure
│   │   ├── db/               # Database layer
│   │   ├── auth/             # Authentication
│   │   ├── utils/            # Utilities
│   │   ├── config.py         # Configuration
│   │   └── main.py           # App entry
│   ├── tests/                # Test files
│   │   ├── test_api/
│   │   ├── test_services/
│   │   └── test_repositories/
│   ├── scripts/              # Utility scripts
│   ├── alembic/              # Database migrations
│   ├── requirements.txt
│   └── ...
│
├── verifiers/                 # Verifier scripts
│   ├── driver.ts
│   ├── compare.ts
│   └── scripts/
│
├── trajectories/              # Playwright trajectories
│   └── trajectory_*.ts
│
├── data_generation/           # Data generation config
│   ├── schema.json
│   └── config.yaml
│
├── Dockerfile                 # Multi-stage build
├── docker-compose.yaml        # Local development
├── gym.config.json           # Gym configuration
├── setup.sh                  # Setup script
├── .cursorrules              # Cursor AI standards
└── README.md                 # This file
```

---

## 📚 API Documentation

### Base URL

- **Development**: http://localhost:8880
- **Production**: Configure via `FRONTEND_URL` environment variable

### Authentication

All endpoints (except `/health`, `/docs`, `/openapi.json`) require authentication via JWT token.

**Login:**
```bash
POST /api/v1/auth/token
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "user@example.com",
  "display_name": "User Name",
  "role": "member",
  "run_id": "uuid-here"
}
```

**Using Token:**
```bash
Authorization: Bearer <access_token>
```

### API Endpoints

#### Health Check
- `GET /health` - Health status (no auth required)

#### Authentication
- `POST /api/v1/auth/token` - Login
- `POST /api/v1/auth/logout` - Logout

#### Users
- `GET /api/v1/users` - List users (paginated, authenticated)
- `GET /api/v1/users/{id}` - Get user (authenticated)
- `POST /api/v1/users` - Create user (admin only)
- `PATCH /api/v1/users/{id}` - Update user (self or admin)
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

### Interactive API Documentation

- **Swagger UI**: http://localhost:8880/docs
- **ReDoc**: http://localhost:8880/redoc
- **OpenAPI JSON**: http://localhost:8880/openapi.json

---

## 🔐 Authentication & Authorization

### Authentication Flow

1. User sends email to `/api/v1/auth/token`
2. Backend validates email in seed database
3. Backend generates unique `run_id` and creates isolated database
4. Backend generates JWT token with user info and `run_id`
5. Frontend stores token and includes in `Authorization: Bearer <token>` header
6. Middleware validates token on each request
7. `run_id` from token is used for database routing

### Authorization (RBAC)

**Roles:**
- **admin**: Full access to all resources
- **member**: Can create/update own resources, read all
- **viewer**: Read-only access

**Using Authorization:**
```python
from app.auth.rbac import require_admin, require_role
from app.auth.dependencies import get_current_user

# Require admin role
@router.delete("/users/{id}", dependencies=[Depends(require_admin())])
def delete_user(id: int):
    ...

# Require specific roles
@router.post("/projects", dependencies=[Depends(require_role(["admin", "member"]))])
def create_project():
    ...

# Get current user (automatically authenticated)
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## 🗄️ Database

### Database Architecture

- **Seed Database**: Template database (`proj3_seed`) used as clone source
- **Run Databases**: Per-run isolated databases (`proj3_{run_id}`)
- **Isolation**: Each user session gets its own database clone

### Database Setup

```bash
# Initialize seed database (first time only)
cd backend
python scripts/init_db.py

# Seed initial data
python scripts/migrate_data.py
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Connection String

```bash
# Development
DATABASE_URL=postgresql+psycopg2://proj3:proj3@localhost:5431/postgres

# Production
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
```

---

## 🐳 Docker & Deployment

### Building Docker Image

```bash
# Build image
docker build -t gym-proj3:latest .

# Build with build arguments
docker build \
  --build-arg NEXT_PUBLIC_API_BASE_PATH=http://localhost:8880 \
  -t gym-proj3:latest .
```

### Running with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Deployment

```bash
# Tag for registry
docker tag gym-proj3:latest registry.company.com/gym-proj3:v1.0.0

# Push to registry
docker push registry.company.com/gym-proj3:v1.0.0

# Deploy (example with Kubernetes)
kubectl set image deployment/gym-proj3 \
  gym-proj3=registry.company.com/gym-proj3:v1.0.0
```

---

## 🤖 Cursor Standards

This project uses Cursor AI for development assistance. The `.cursorrules` file contains standards that Cursor follows.

### Key Standards

1. **Code Quality First**: Clean, maintainable, well-documented code
2. **Type Safety**: Type hints in Python, TypeScript types in frontend
3. **Test Coverage**: >80% coverage required
4. **Security**: Always validate inputs, use authentication
5. **Error Handling**: Graceful error handling with proper messages
6. **Documentation**: Document complex logic and APIs

### Cursor Rules Summary

**Backend:**
- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 100 characters
- Use Pydantic for validation
- Use dependency injection
- Write tests for all new code

**Frontend:**
- Use TypeScript strict mode
- Functional components with hooks
- Named exports preferred
- Test with React Testing Library
- Use React Query for data fetching

**General:**
- Never commit secrets
- Use proper HTTP status codes
- Write descriptive commit messages
- Document all public APIs
- Follow security best practices

**See `.cursorrules` file for complete standards.**

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Database connection failed**
```bash
# Check PostgreSQL is running
docker-compose ps

# Check DATABASE_URL environment variable
echo $DATABASE_URL

# Test connection
psql -h localhost -U proj3 -d postgres
```

**Issue: Port already in use**
```bash
# Find process using port
lsof -i :5173  # Frontend
lsof -i :8880  # Backend

# Kill process
kill -9 <PID>
```

**Issue: Module not found**
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

**Issue: Authentication fails**
```bash
# Check JWT_SECRET_KEY is set
echo $JWT_SECRET_KEY

# Verify token format
# Token should be in Authorization header: Bearer <token>
```

**Issue: Tests failing**
```bash
# Run tests with verbose output
pytest -v

# Check test database setup
# Ensure test fixtures are properly configured
```

---

## 📝 Development Workflow

### 1. Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-new-endpoint
```

### 2. Develop Feature

- Write code following standards
- Write tests (aim for >80% coverage)
- Update documentation
- Test locally

### 3. Commit Changes

```bash
# Use conventional commits
git commit -m "feat: add user profile endpoint"
git commit -m "test: add tests for user profile"
git commit -m "docs: update API documentation"
```

### 4. Create Pull Request

- Push branch: `git push origin feature/add-new-endpoint`
- Create PR to `develop` branch
- Ensure all tests pass
- Request code review

### 5. Code Review Checklist

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] Test coverage >80%
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Error handling implemented
- [ ] Type hints/types used
- [ ] Security considerations addressed

---

## 📖 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/
- **React Docs**: https://react.dev/learn
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Pydantic Docs**: https://docs.pydantic.dev/

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review `.cursorrules` for coding standards
3. Check API docs at `/docs`
4. Review test files for examples
5. Contact team lead

---

**Last Updated**: {DATE}  
**Gym Version**: 1.0.0  
**Backend Version**: 1.0.0  
**Frontend Version**: 1.0.0
