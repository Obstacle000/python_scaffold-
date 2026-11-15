"""关系型数据库异步连接池管理器 (支持 MySQL / SQLite)."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.agent.config import MYSQL_DSN, DEBUG


class DatabaseClientManager:
    """管理 SQLAlchemy 异步引擎与 Session 会话工厂."""

    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    def init(self, dsn: str | None = None) -> None:
        """初始化异步数据库引擎."""
        if self.engine is not None:
            return
        target_dsn = dsn or MYSQL_DSN
        kwargs: dict = {"echo": DEBUG, "pool_pre_ping": True}
        if not target_dsn.startswith("sqlite"):
            kwargs["pool_size"] = 10
            kwargs["max_overflow"] = 20

        self.engine = create_async_engine(target_dsn, **kwargs)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        """安全关闭连接池释放资源."""
        if self.engine is not None:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None


database_client_manager = DatabaseClientManager()
mysql_client_manager = database_client_manager
