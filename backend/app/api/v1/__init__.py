"""API v1 package for proj3."""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, users

router = APIRouter()

# Include sub-routers
router.include_router(auth.router, tags=["auth"])
router.include_router(users.router, tags=["users"])


