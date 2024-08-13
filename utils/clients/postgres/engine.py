from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import DatabaseClientConfig
from utils.common.cache import async_cache


@async_cache(60 * 30)
async def get_postgres_engine(config: DatabaseClientConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        config.postgres_url,
        echo=True,
        future=True,
        pool_size=20,
        max_overflow=30,
    )
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
