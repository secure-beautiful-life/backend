from typing import Type, List, Optional

from app.product.model import Category
from app.product.repository import CategoryRepo
from core.exceptions import BadRequestException


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepo()

    async def get_category_by_id(self, category_id: int):
        category = await self.category_repo.get_by_id(category_id)

        if category is None:
            raise BadRequestException("해당하는 카테고리 아이디를 찾을 수 없습니다.")

        return category

    async def get_category_list_with_children(self) -> List[Type[Category]]:
        return await self.category_repo.get_category_list_with_children()

    async def create_category(self, name: str, parent_id: Optional[int] = None) -> Optional[int]:
        # 카테고리 깊이 가져오기
        depth = await self.get_depth(parent_id)

        category = await self.category_repo.save(
            model=Category(
                parent_id=parent_id,
                name=name,
                depth=depth
            )
        )

        return category.id

    async def delete_category(self, category_id: int):
        return await self.category_repo.delete_by_id(category_id)

    async def get_depth(self, parent_id: Optional[int] = None):
        if parent_id is None:
            return 0

        parent_category = await self.get_category_by_id(parent_id)
        depth = parent_category.depth + 1

        return depth
