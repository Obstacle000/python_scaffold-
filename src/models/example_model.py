"""示例 ORM 模型 (用于 MySQL / SQLite 关系型数据库演示)."""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimeStampedMixin


class ExampleModel(Base, TimeStampedMixin):
    """示例业务实体表."""

    __tablename__ = "example_items"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="条目标题",
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default="",
        comment="条目详细内容",
    )
