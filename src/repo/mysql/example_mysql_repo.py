"""MySQL / 关系型数据库仓储示例."""

from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import ExampleModel
from src.repo.base_repo import BaseRepository


class ExampleMySQLRepository(BaseRepository[ExampleModel]):
    """处理 ExampleModel 在关系型数据库中的持久化与查询."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model_class=ExampleModel, session=session)

    async def get_by_title(self, title: str) -> Optional[ExampleModel]:
        """按标题精确查找记录."""
        stmt = select(self.model).where(
            self.model.title == title,
            self.model.is_deleted.is_(False),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_active(self, skip: int = 0, limit: int = 20) -> Sequence[ExampleModel]:
        """查询未软删除的有效记录列表."""
        stmt = (
            select(self.model)
            .where(self.model.is_deleted.is_(False))
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
