from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from utils.clients.postgres.abstract_model import AbstractModel
from utils.clients.postgres.query import build_query
from utils.clients.postgres.types import ColumnExpressionType


class UpdateModel(AbstractModel):
    __abstract__ = True

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            clause_filter: ColumnExpressionType,
            **kwargs
    ) -> Self:
        query = cls.__table__.update().values(**kwargs).returning(cls)
        query = await build_query(query, clause_filter=clause_filter)

        result = await session.execute(query)
        await session.commit()

        return cls(**result.mappings().first())
