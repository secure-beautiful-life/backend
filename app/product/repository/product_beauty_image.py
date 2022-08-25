from app.product.model.product_beauty_image import ProductBeautyImage
from core.repository import BaseRepoORM


class ProductBeautyImageRepo(BaseRepoORM):
    model = ProductBeautyImage