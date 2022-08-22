from app.product.model import ProductDetailImage
from core.repository import BaseRepoORM


class ProductDetailImageRepo(BaseRepoORM):
    model = ProductDetailImage
