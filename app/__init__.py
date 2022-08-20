from fastapi import APIRouter

from app.auth.router import auth_router
from app.user.router import user_router

router = APIRouter()
router.include_router(user_router, prefix="/api/users", tags=["User"])
router.include_router(auth_router, prefix="/api/auth", tags=["Auth"])

__all__ = ["router"]
