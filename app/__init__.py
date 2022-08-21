from fastapi import APIRouter

from app.auth.router import auth_router
from app.user.router import user_router
from app.product.router import category_router, product_router

router = APIRouter()
router.include_router(user_router, prefix="/api/users", tags=["User"])
router.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
router.include_router(category_router, prefix="/api/categories", tags=["Category"])
router.include_router(product_router, prefix="/api/products", tags=["Product"])

__all__ = ["router"]
