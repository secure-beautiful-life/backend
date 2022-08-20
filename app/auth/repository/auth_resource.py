from typing import Optional, Type

from sqlalchemy import select

from app.auth.model import AuthResource
from core.db import session
from core.repository import BaseRepoORM


class AuthResourceRepo(BaseRepoORM):
    model = AuthResource

    @classmethod
    async def get_resource_list(cls, limit: int = 10, offset: Optional[int] = None, method: Optional[str] = None) -> \
            Optional[Type[AuthResource]]:
        query = select(cls.model)

        if method:
            query = query.filter_by(method=method)

        if offset:
            query = query.offset(offset * limit)

        if limit > 100:
            limit = 100

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
