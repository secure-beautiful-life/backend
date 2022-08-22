from app.product.model import ProductProfileImage
from core.repository import BaseRepoORM


class ProductProfileImageRepo(BaseRepoORM):
    model = ProductProfileImage
