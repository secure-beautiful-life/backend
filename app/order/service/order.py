from typing import Optional, Type, List

from app.order.model import Order, OrderDetail
from app.order.repository import OrderRepo, OrderDetailRepo
from app.product.service import ProductService
from app.user.service import UserService
from core.exceptions import NotFoundException, BadRequestException, ForbiddenException
import requests
import json

class OrderService:
    def __init__(self):
        self.repo = OrderRepo()
        self.detail_repo = OrderDetailRepo()

    async def create_order_with_user_id(self, user_id: int, products: list, address: str) -> Optional[int]:
        user = await UserService().get_user_by_id(id=user_id)
        user_name = user.info[0].name

        for product in products:
            product_ = await ProductService().get_product_by_id(product_id=product["id"])
            if not product_:
                raise NotFoundException(message="해당하는 상품 아이디를 찾을 수 없습니다.")

            if product_.stock_quantity < product["amount"]:
                raise BadRequestException(message="주문하신 상품의 재고가 부족합니다.")

            product["price"] = product_.price

        order = await self.repo.save(model=Order(user_id=user_id, status="ORDERED", address=address))
        order_id = order.id

        total_price = 0

        for product in products:
            await self.detail_repo.save(model=OrderDetail(
                order_id=order_id,
                product_id=product["id"],
                price=product["price"],
                amount=product["amount"]
            ))
            total_price += product["price"]

        await self.kakaotalk_send(f'{user_name}님이 상품을 주문했습니다. 총 상품의 가격은 {total_price}입니다.')

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

    async def kakaotalk_send(self, text):
        access_token = "3ycS7YY9kO6rvGAIqvN0iuBuVvezk2-7KJWiWArxCinJXwAAAYLXr60x"

        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

        headers = {
            "Authorization": "Bearer " + access_token
        }

        data = {
            'object_type': 'text',
            'text': text,
            'link': {
                'web_url': 'https://developers.kakao.com',
                'mobile_web_url': 'https://developers.kakao.com'
            },
            'button_title': '주문'
        }

        data = {'template_object': json.dumps(data)}
        response = requests.post(url, headers=headers, data=data)

        return response