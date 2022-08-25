from fastapi import APIRouter

from app.auth.router import auth_router
from app.beauty.router import beauty_router
from app.cart.router import cart_router
from app.order.router import order_router
from app.product.router import category_router, product_router, product_wish_router
from app.review.router import review_router
from app.user.router import user_router

router = APIRouter()
router.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
router.include_router(user_router, prefix="/api/users", tags=["User"])
router.include_router(category_router, prefix="/api/categories", tags=["Category"])
router.include_router(product_router, prefix="/api/products", tags=["Product"])
router.include_router(product_wish_router, prefix="/api/wishes", tags=["Wish"])
router.include_router(cart_router, prefix="/api/carts", tags=["Cart"])
router.include_router(order_router, prefix="/api/orders", tags=["Order"])
router.include_router(review_router, prefix="/api/reviews", tags=["Review"])
router.include_router(beauty_router, prefix="/api/beauties", tags=["Beauty"])

__all__ = ["router"]
