"""通用的泛型数据访问仓储基类 (Repository Pattern)."""

from typing import Generic, TypeVar, Type, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """提供通用的异步数据库增删改查操作."""

    def __init__(self, model_class: Type[ModelType], session: AsyncSession) -> None:
        self.model = model_class
        self.session = session

    async def get_by_id(self, id_val: int) -> Optional[ModelType]:
        """根据主键 ID 查询单条记录."""
        result = await self.session.execute(
            select(self.model).where(getattr(self.model, "id") == id_val)
        )
        return result.scalars().first()

    async def list_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """分页获取所有记录."""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, instance: ModelType) -> ModelType:
        """新增单条记录并刷新."""
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete_by_id(self, id_val: int) -> bool:
        """物理删除指定 ID 记录."""
        result = await self.session.execute(
            delete(self.model).where(getattr(self.model, "id") == id_val)
        )
        return result.rowcount > 0
