from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Optional

from sqlalchemy import select, update, delete, func

from core.db.session import Base, session
from core.repository.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepo(ABC):
    @classmethod
    @abstractmethod
    async def safe_commit(cls, query: Any = None, model: Optional[ModelType] = None) -> Optional[ModelType]:
        pass

    @classmethod
    @abstractmethod
    async def save(cls, model: Optional[ModelType]) -> Optional[ModelType]:
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
    async def filter_by(cls, params: dict) -> Optional[ModelType]:
        pass

    @classmethod
    @abstractmethod
    async def filter_by_list(cls, params: dict, limit: int = 10, offset: Optional[int] = None) -> Optional[ModelType]:
        pass

    @classmethod
    @abstractmethod
    async def count_all(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    async def update_by_id(cls, id: int, params: dict, synchronize_session: SynchronizeSessionEnum = False) -> int:
        pass

    @classmethod
    @abstractmethod
    async def delete_by_id(cls, id: int, synchronize_session: SynchronizeSessionEnum = False) -> int:
        pass


class BaseRepoORM(BaseRepo):
    @classmethod
    async def safe_commit(cls, query: Any = None, model: Optional[ModelType] = None) -> Optional[ModelType]:
        try:
            if not ((query is None) is not (model is None)):
                raise ValueError("Safe commit error")
            if query is not None:
                await session.execute(query)
                await session.commit()
            if model:
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return model
        except Exception as e:
            await session.rollback()
            raise e

    @classmethod
    async def save(cls, model: Optional[ModelType]) -> Optional[ModelType]:
        return await cls.safe_commit(model=model)

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
    async def get_list_desc(cls, limit: int = 10, offset: Optional[int] = None) -> List[ModelType]:
        query = select(cls.model)

        if offset:
            query = query.offset(offset * limit)

        if limit > 100:
            limit = 100

        query = query.limit(limit)
        query = query.order_by(cls.model.id.desc())

        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def filter_by(cls, params: dict) -> Optional[ModelType]:
        query = select(cls.model).filter_by(**params)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def filter_by_list(cls, params: dict, limit: int = 10, offset: Optional[int] = None) -> Optional[ModelType]:
        query = select(cls.model).filter_by(**params)

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
    async def update_by_id(cls, id: int, params: dict, synchronize_session: SynchronizeSessionEnum = False) -> int:
        query = (
            update(cls.model)
            .where(cls.model.id == id)
            .values(params)
            .execution_options(synchronize_session=synchronize_session)
        )
        await cls.safe_commit(query)
        return id

    @classmethod
    async def delete_by_id(cls, id: int, synchronize_session: SynchronizeSessionEnum = False) -> int:
        query = (
            delete(cls.model)
            .where(cls.model.id == id)
            .execution_options(synchronize_session=synchronize_session)
        )
        await cls.safe_commit(query)
        return id
