import os
from typing import Optional, Type, List

from app.product.service import ProductService
from app.review.model import Review, ReviewImage
from app.review.repository import ReviewRepo, ReviewImageRepo
from app.user.service import UserService
from core.config import config
from core.exceptions import BadRequestException, NotFoundException, ForbiddenException
from core.utils import ImageHelper

MAX_REVIEW_IMAGE_UPLOAD_AMOUNT = 5


class ReviewService:
    def __init__(self):
        self.repo = ReviewRepo()
        self.image_repo = ReviewImageRepo()

    async def create_review(self, user_id: int, product_id: int, content: str, images: list, rate: int) -> int:
        await UserService().get_user_by_id(id=user_id)
        await ProductService().get_product_by_id(product_id=product_id)

        if len(images) > MAX_REVIEW_IMAGE_UPLOAD_AMOUNT:
            raise BadRequestException(f"리뷰 이미지는 최대 {MAX_REVIEW_IMAGE_UPLOAD_AMOUNT}장까지 업로드 할 수 있습니다.")

        image_size_list, image_type_list, saved_name_list = ImageHelper.upload_images(
            images,
            config.REVIEW_IMAGE_DIR
        )

        review = await self.repo.save(
            Review(
                user_id=user_id,
                product_id=product_id,
                content=content,
                rate=rate
            )
        )
        review_id = review.id

        for idx, image in enumerate(images):
            await self.image_repo.save(
                ReviewImage(
                    review_id=review_id,
                    uploaded_name=image["file_name"],
                    saved_name=saved_name_list[idx],
                    size=image_size_list[idx],
                    type=image_type_list[idx]
                )
            )

        return review_id

    async def get_review_by_id(self, id: int) -> Optional[Type[Review]]:
        review = await self.repo.get_by_id(id=id)
        if not review:
            raise NotFoundException(message="존재하지 않는 리뷰 id입니다.")

        return review

    async def get_review_list_with_product_id(self, product_id: int, limit: int = 10, offset: Optional[int] = None) -> \
            List[Type[Review]]:
        await ProductService().get_product_by_id(product_id=product_id)
        return await self.repo.filter_by_list(params=dict(product_id=product_id), limit=limit, offset=offset)

    async def get_review_count_with_product_id(self, product_id: int) -> Optional[int]:
        return await self.repo.count_review_with_product_id(product_id=product_id)

    async def delete_review_by_id(self, user_id: int, id: int) -> Optional[int]:
        review = await self.get_review_by_id(id=id)
        if user_id != review.user_id:
            raise ForbiddenException(message="본인의 리뷰만 삭제할 수 있습니다.")

        images = await self.image_repo.filter_by_list(params=dict(review_id=id))
        if images:
            for image in images:
                image_id = image.id
                image_path = os.path.join(config.REVIEW_IMAGE_DIR, image.saved_name)
                if os.path.exists(image_path):
                    os.remove(image_path)
                await self.image_repo.delete_by_id(id=image_id)

        return await self.repo.delete_by_id(id=id)
