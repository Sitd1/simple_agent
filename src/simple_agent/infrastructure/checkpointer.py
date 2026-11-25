from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from simple_agent.config.storage_config import StorageConfig


@asynccontextmanager
async def manage_sqlite_checkpointer(
    config: StorageConfig | None = None
    ) -> AsyncIterator[AsyncSqliteSaver]:
    cfg = config or StorageConfig()
    cfg.ensure_dir()
    async with AsyncSqliteSaver.from_conn_string(cfg.sqlite_path) as saver:
        yield saver
