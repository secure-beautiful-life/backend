from typing import Optional, Type, List

from app.cart.model import Cart
from app.cart.repository import CartRepo
from app.product.service import ProductService
from app.user.service import UserService
from core.exceptions import NotFoundException


class CartService:
    def __init__(self):
        self.repo = CartRepo()

    async def create_cart_with_user_id(self, user_id: int, product_id: int, amount: int) -> Optional[int]:
        await UserService().get_user_by_id(id=user_id)
        await ProductService().get_product_by_id(product_id=product_id)

        prev_cart = await self.repo.filter_by(params=dict(user_id=user_id, product_id=product_id))
        if prev_cart:
            return await self.repo.update_by_id(id=prev_cart.id, params=dict(amount=prev_cart.amount + amount))

        return await self.repo.save(model=Cart(user_id=user_id, product_id=product_id, amount=amount))

    async def get_cart_list_with_user_id(self, user_id: int, limit: int = 10, offset: Optional[int] = None) -> \
            List[Type[Cart]]:
        await UserService().get_user_by_id(id=user_id)
        return await self.repo.filter_by_list(params=dict(user_id=user_id), limit=limit, offset=offset)

    async def get_cart_count_with_user_id(self, user_id: int) -> Optional[int]:
        return await self.repo.cart_count_with_user_id(user_id=user_id)

    async def get_cart_by_id(self, id: int) -> Optional[Type[Cart]]:
        cart = await self.repo.get_by_id(id=id)
        if not cart:
            raise NotFoundException(message="존재하지 않는 장바구니 id입니다.")
        return cart

    async def update_cart_by_id(self, id: int, amount: int) -> Optional[int]:
        await self.get_cart_by_id(id=id)
        return await self.repo.update_by_id(id=id, params=dict(amount=amount))

    async def delete_cart_by_id(self, id: int) -> Optional[int]:
        await self.get_cart_by_id(id=id)
        return await self.repo.delete_by_id(id=id)

    async def truncate_cart_by_user_id(self, user_id: int) -> None:
        if not self.get_cart_list_with_user_id(user_id=user_id):
            raise NotFoundException(message="장바구니에 삭제할 항목이 존재하지 않습니다.")
        await self.repo.truncate_cart_by_user_id(user_id=user_id)
