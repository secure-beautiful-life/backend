from app.order.model import OrderDetail
from core.repository import BaseRepoORM


class OrderDetailRepo(BaseRepoORM):
    model = OrderDetail
