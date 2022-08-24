from fastapi import APIRouter

from app.auth.router import auth_router
from app.cart.router import cart_router
from app.order.router import order_router
from app.product.router import category_router, product_router, product_wish_router
from app.user.router import user_router

router = APIRouter()
router.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
router.include_router(cart_router, prefix="/api/carts", tags=["Cart"])
router.include_router(order_router, prefix="/api/orders", tags=["Order"])
router.include_router(user_router, prefix="/api/users", tags=["User"])
router.include_router(category_router, prefix="/api/categories", tags=["Category"])
router.include_router(product_router, prefix="/api/products", tags=["Product"])
router.include_router(product_wish_router, prefix="/api/wishes", tags=["Wish"])

__all__ = ["router"]
