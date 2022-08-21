from app.product.model import ProductWish
from app.product.repository import ProductWishRepo, ProductRepo
from core.exceptions import BadRequestException


class ProductWishService:
    def __init__(self):
        self.product_wish_repo = ProductWishRepo()
        self.product_repo = ProductRepo()

    async def exists_wish(self, user_id: int, product_id: int):
        return await self.product_wish_repo.exists_wish(user_id, product_id)

    async def get_wish_list(self, user_id: int):
        return await self.product_wish_repo.filter_by_list({"user_id": user_id}, 100)

    async def create_wish(self, user_id: int, product_id: int):
        if await self.exists_wish(user_id, product_id):
            raise BadRequestException("이미 상품 좋아요를 누른 상품입니다.")

        await self.product_wish_repo.save(
            ProductWish(user_id=user_id, product_id=product_id)
        )

        return await self.product_repo.get_by_id(id=product_id)

    async def delete_wish(self, user_id: int, product_id: int):
        await self.product_wish_repo.delete_wish(user_id=user_id, product_id=product_id)

        return await self.product_repo.get_by_id(id=product_id)
