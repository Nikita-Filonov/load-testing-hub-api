from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings, get_settings
from utils.clients.postgres.engine import get_postgres_engine


async def get_postgres_session(settings: Annotated[Settings, Depends(get_settings)]) -> AsyncSession:
    async_session = await get_postgres_engine(settings.postgres)

    async with async_session() as session:
        yield session
