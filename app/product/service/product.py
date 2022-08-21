import os
import uuid
from base64 import b64decode
from io import BytesIO
from typing import Optional, List

from PIL import Image

from app.product.model import Product, ProductProfileImage, ProductDetailImage
from app.product.repository import ProductRepo, ProductProfileImageRepo, ProductDetailImageRepo
from core.config import config
from core.exceptions import BadRequestException, ForbiddenException

MAX_DETAIL_IMAGE_UPLOAD_SIZE = 5


class ProductService:
    def __init__(self):
        self.product_repo = ProductRepo()
        self.product_profile_image_repo = ProductProfileImageRepo()
        self.product_detail_image_repo = ProductDetailImageRepo()

    async def get_product_by_id(self, product_id: int):
        product = await self.product_repo.get_by_id(product_id)

        if product is None:
            raise BadRequestException("해당하는 상품 아이디를 찾을 수 없습니다.")

        return product

    async def get_product_list_by_filter(self, limit: int = 10, offset: Optional[int] = None,
                                         category_id: Optional[int] = None) -> List[Product]:
        return await self.product_repo.get_product_list_by_filter_desc(limit=limit,
                                                                       offset=offset,
                                                                       category_id=category_id)

    async def get_product_list_search_autocomplete(self, limit: int = 10, offset: Optional[int] = None,
                                                   name: str = "") -> List[Product]:
        return await self.product_repo.get_product_list_search_autocomplete_desc(limit=limit, offset=offset, name=name)

    async def get_product_filter_count(self, category_id: int = None) -> int:
        return await self.product_repo.get_product_filter_count(category_id=category_id)

    async def get_product_list_search_count(self, name: str = "") -> int:
        return await self.product_repo.get_product_list_search_count(name=name)

    async def create_product(self, user_id: int, category_id: int, profile_image_string: str, profile_file_name: str,
                             name: str, price: int, stock_quantity: int, detail_images) -> int:
        if len(detail_images) > MAX_DETAIL_IMAGE_UPLOAD_SIZE:
            raise BadRequestException("상품 상세 이미지는 최대 5장까지 업로드 할 수 있습니다.")

        image_size, image_type, saved_name = await self.upload_image(profile_image_string)
        image_size_list, image_type_list, saved_name_list = await self.upload_images(detail_images)

        product = await self.product_repo.save(
            Product(
                user_id=user_id,
                category_id=category_id,
                name=name,
                price=price,
                stock_quantity=stock_quantity,
            )
        )
        product_id = product.id

        await self.product_profile_image_repo.save(
            ProductProfileImage(
                product_id=product_id,
                uploaded_name=profile_file_name,
                saved_name=saved_name,
                size=image_size,
                type=image_type
            )
        )

        for index, detail_image in enumerate(detail_images):
            detail_file_name = detail_image['file_name']

            await self.product_detail_image_repo.save(
                ProductDetailImage(
                    product_id=product_id,
                    uploaded_name=detail_file_name,
                    saved_name=saved_name_list[index],
                    size=image_size_list[index],
                    type=image_type_list[index]
                )
            )

        return product_id

    async def update_product(self, user_id: int, product_id: int, name: Optional[str] = None,
                             price: Optional[int] = None):
        product = await self.product_repo.get_by_id(id=product_id)

        if self.has_not_product(product):
            raise BadRequestException("해당하는 상품 아이디를 찾을 수 없습니다.")

        if self.is_same_not_seller(user_id, product.user_id):
            raise ForbiddenException("상품 판매자만 상품을 삭제할 수 있습니다.")

        params = {}
        if name:
            params["name"] = name

        if price:
            params["price"] = price

        return await self.product_repo.update_by_id(product_id, params=params)

    async def delete_product(self, user_id: int, product_id: int):
        product = await self.product_repo.get_by_id(id=product_id)

        if self.has_not_product(product):
            raise BadRequestException("해당하는 상품 아이디를 찾을 수 없습니다.")

        if self.is_same_not_seller(user_id, product.user_id):
            raise ForbiddenException("상품 판매자만 상품을 삭제할 수 있습니다.")

        return await self.product_repo.delete_by_id(product_id)

    def has_not_product(self, product):
        return not product

    def is_same_not_seller(self, user_id, product_id):
        return user_id != product_id

    async def upload_image(self, image_string):
        try:
            image_string = image_string[image_string.find(",") + 1:]
            image = Image.open(BytesIO(b64decode(image_string)))
        except Exception:
            raise BadRequestException(message="유효하지 않은 이미지입니다.")

        image_type = image.format
        if image_type not in config.ALLOWED_IMAGE_TYPES:
            raise BadRequestException(message="허용되지 않은 이미지 형식입니다.")

        buffer = BytesIO()
        image.save(buffer, format=image_type)
        image_size = buffer.tell()

        if image_size > config.MAX_IMAGE_SIZE:
            raise BadRequestException(message="이미지 크기가 허용치를 초과하였습니다.")

        saved_name = f"{uuid.uuid4()}.{image_type}"
        saved_path = os.path.join(config.PRODUCT_IMAGE_DIR, saved_name)

        with open(saved_path, "wb") as f:
            f.write(buffer.getbuffer().tobytes())

        return image_size, image_type, saved_name

    async def upload_images(self, detail_images):
        image_size_list, image_type_list, saved_name_list = [], [], []

        for detail_image in detail_images:
            image_string, file_name = detail_image['image_string'], detail_image['file_name']
            image_size, image_type, saved_name = await self.upload_image(image_string)
            image_size_list.append(image_size), image_type_list.append(image_type), saved_name_list.append(saved_name)

        return image_size_list, image_type_list, saved_name_list
