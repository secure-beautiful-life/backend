from typing import Optional, Type, List

from app.order.model import Order, OrderDetail
from app.order.repository import OrderRepo, OrderDetailRepo
from app.product.service import ProductService
from app.user.service import UserService
from core.exceptions import NotFoundException, BadRequestException, ForbiddenException


class OrderService:
    def __init__(self):
        self.repo = OrderRepo()
        self.detail_repo = OrderDetailRepo()

    async def create_order_with_user_id(self, user_id: int, products: list, address: str) -> Optional[int]:
        await UserService().get_user_by_id(id=user_id)

        for product in products:
            product_ = await ProductService().get_product_by_id(product_id=product["id"])
            if not product_:
                raise NotFoundException(message="해당하는 상품 아이디를 찾을 수 없습니다.")

            if product_.stock_quantity < product["amount"]:
                raise BadRequestException(message="주문하신 상품의 재고가 부족합니다.")

            product["price"] = product_.price

        order = await self.repo.save(model=Order(user_id=user_id, status="ORDERED", address=address))
        order_id = order.id

        for product in products:
            await self.detail_repo.save(model=OrderDetail(
                order_id=order_id,
                product_id=product["id"],
                price=product["price"],
                amount=product["amount"]
            ))

        return order_id

    async def get_order_list_with_user_id(self, user_id: int, limit: int = 10, offset: Optional[int] = None) -> \
            List[Type[Order]]:
        await UserService().get_user_by_id(id=user_id)
        return await self.repo.filter_by_list(params=dict(user_id=user_id), limit=limit, offset=offset)

    async def get_order_count_with_user_id(self, user_id: int) -> Optional[int]:
        return await self.repo.count_order_with_user_id(user_id=user_id)

    async def get_order_by_id(self, id: int) -> Optional[Type[Order]]:
        order = await self.repo.get_by_id(id=id)
        if not order:
            raise NotFoundException(message="존재하지 않는 주문 id입니다.")
        return order

    async def cancel_order_by_id(self, user_id: int, id: int) -> Optional[int]:
        order = await self.get_order_by_id(id=id)
        if user_id != order.user_id:
            raise ForbiddenException(message="본인의 주문만 수정할 수 있습니다.")
        return await self.repo.update_by_id(id=id, params=dict(status="CANCELED"))
