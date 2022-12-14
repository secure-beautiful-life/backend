import os
from typing import Optional, List

from app.product.model import Product, ProductProfileImage, ProductDetailImage
from app.product.model.product_beauty_image import ProductBeautyImage
from app.product.repository import ProductRepo, ProductProfileImageRepo, ProductDetailImageRepo
from app.product.repository.product_beauty_image import ProductBeautyImageRepo
from app.user.service import UserService
from core.config import config
from core.exceptions import BadRequestException, ForbiddenException
from core.utils import ImageHelper, GmailHelper

MAX_DETAIL_IMAGE_UPLOAD_SIZE = 5


class ProductService:
    def __init__(self):
        self.product_repo = ProductRepo()
        self.product_profile_image_repo = ProductProfileImageRepo()
        self.product_detail_image_repo = ProductDetailImageRepo()
        self.product_beauty_image_repo = ProductBeautyImageRepo()

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
                             name: str, price: int, stock_quantity: int, detail_images,
                             beauty_image_string: str, beauty_file_name: str) -> int:
        await UserService().get_user_by_id(user_id)

        if len(detail_images) > MAX_DETAIL_IMAGE_UPLOAD_SIZE:
            raise BadRequestException("상품 상세 이미지는 최대 5장까지 업로드 할 수 있습니다.")

        image_size, image_type, saved_name = ImageHelper.upload_image(profile_image_string, config.PRODUCT_IMAGE_DIR)
        image_size_list, image_type_list, saved_name_list = ImageHelper.upload_images(
            detail_images,
            config.PRODUCT_IMAGE_DIR
        )
        beauty_image_size, beauty_image_type, beauty_saved_name = ImageHelper \
            .upload_image(beauty_image_string, config.PRODUCT_IMAGE_DIR)

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

        await self.product_beauty_image_repo.save(
            ProductBeautyImage(
                product_id=product_id,
                uploaded_name=beauty_file_name,
                saved_name=beauty_saved_name,
                size=beauty_image_size,
                type=beauty_image_type
            )
        )

        return product_id

    async def update_product(self, user_id: int, product_id: int, name: Optional[str] = None,
                             price: Optional[int] = None):
        await UserService().get_user_by_id(user_id)

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
        await UserService().get_user_by_id(user_id)

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

    def send_product_image_to_email(self, destination: str, image_string: str):
        image_size, image_type, saved_name = ImageHelper.upload_image(image_string, config.PRODUCT_IMAGE_DIR)
        GmailHelper.send_message(
            destination=destination,
            subject="Beautiful Life 화이팅!",
            body="소개딩 화이팅!",
            attachments=[os.path.join(config.PRODUCT_IMAGE_DIR, saved_name)]
        )
