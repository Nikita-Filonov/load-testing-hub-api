from typing import Self

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from utils.clients.postgres.abstract_model import AbstractModel


class CreateModel(AbstractModel):
    __abstract__ = True

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> Self:
        query = insert(cls).values(**kwargs).returning(cls)

        result = await session.execute(query)
        await session.commit()

        return result.scalars().first()
