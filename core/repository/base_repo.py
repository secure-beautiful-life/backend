from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Optional

from core.db.session import Base, session
from sqlalchemy import insert, select, update, delete, func

from core.repository.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepo(ABC):
    @classmethod
    @abstractmethod
    async def safe_commit(cls, query: Any) -> None:
        pass

    @classmethod
    @abstractmethod
    async def save(cls, params: dict) -> None:
        pass

    @classmethod
    @abstractmethod
    async def get_by_id(cls, id: int) -> Optional[ModelType]:
        pass

    @classmethod
    @abstractmethod
    async def get_list(cls, limit: int = 10, offset: Optional[int] = None) -> List[ModelType]:
        pass

    @classmethod
    @abstractmethod
    async def count_all(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    async def update_by_id(cls, id: int, params: dict, synchronize_session: SynchronizeSessionEnum = False) -> None:
        pass

    @classmethod
    @abstractmethod
    async def delete_by_id(cls, id: int, synchronize_session: SynchronizeSessionEnum = False) -> None:
        pass


class BaseRepoORM(BaseRepo):
    @classmethod
    async def safe_commit(cls, query: Any) -> None:
        try:
            await session.execute(query)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

    @classmethod
    async def save(cls, params: dict) -> None:
        query = insert(cls.model).values(params)
        await cls.safe_commit(query)

    @classmethod
    async def get_by_id(cls, id: int) -> Optional[ModelType]:
        query = select(cls.model).where(cls.model.id == id)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def get_list(cls, limit: int = 10, offset: Optional[int] = None) -> List[ModelType]:
        query = select(cls.model)

        if offset:
            query = query.offset(offset * limit)

        if limit > 100:
            limit = 100

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def count_all(cls) -> int:
        query = func.count(cls.model.id)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def update_by_id(cls, id: int, params: dict, synchronize_session: SynchronizeSessionEnum = False) -> None:
        query = (
            update(cls.model)
            .where(cls.model.id == id)
            .values(params)
            .execution_options(synchronize_session=synchronize_session)
        )
        await cls.safe_commit(query)

    @classmethod
    async def delete_by_id(cls, id: int, synchronize_session: SynchronizeSessionEnum = False) -> None:
        query = (
            delete(cls.model)
            .where(cls.model.id == id)
            .execution_options(synchronize_session=synchronize_session)
        )
        await cls.safe_commit(query)
