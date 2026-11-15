"""SQLAlchemy ORM 基础模型与通用字段 Mixin."""

from datetime import datetime, timezone
from sqlalchemy import BigInteger, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    """获取当前 UTC 时间."""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """所有 ORM 模型的声明式基类."""
    pass


class TimeStampedMixin:
    """通用审计与软删除字段混入类 (Mixin)."""

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键自增 ID",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        comment="创建时间",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        comment="最后更新时间",
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="逻辑删除标记",
    )
