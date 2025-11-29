from alembic import command
from typing import AsyncGenerator
from alembic.config import Config
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import TEST_DATABASE, TEST_SYNC_DATABASE

engine = create_async_engine(
    TEST_DATABASE,
    pool_pre_ping=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


def run_migrations() -> None:
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_SYNC_DATABASE)
    command.upgrade(alembic_cfg, "head")
