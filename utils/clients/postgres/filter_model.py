from typing import Self, Sequence

from sqlalchemy import select, func, ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession

from utils.clients.postgres.abstract_model import AbstractModel
from utils.clients.postgres.query import build_query
from utils.clients.postgres.types import ColumnExpressionType


class FilterModel(AbstractModel):
    __abstract__ = True

    @classmethod
    async def get(
            cls,
            session: AsyncSession,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> Self | None:
        query = select(cls).filter_by(**kwargs)
        query = await build_query(query, clause_filter=clause_filter)

        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def filter(
            cls,
            session: AsyncSession,
            limit: int | None = None,
            offset: int | None = None,
            distinct: ColumnExpressionType | None = None,
            order_by: ColumnExpressionType | None = None,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> Sequence[Self]:
        query = select(cls).filter_by(**kwargs)
        query = await build_query(
            query,
            limit=limit,
            offset=offset,
            distinct=distinct,
            order_by=order_by,
            clause_filter=clause_filter
        )

        result = await session.execute(query)

        return result.scalars().all()

    @classmethod
    async def count(
            cls,
            session: AsyncSession,
            column: ColumnExpressionArgument,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> int:
        query = select(func.count(column)).filter_by(**kwargs)
        query = await build_query(query, clause_filter=clause_filter)

        return await session.scalar(query)

    @classmethod
    async def average(
            cls,
            session: AsyncSession,
            column: ColumnExpressionArgument,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> float | None:
        query = select(func.avg(column)).filter_by(**kwargs)
        query = await build_query(query, clause_filter=clause_filter)

        return await session.scalar(query)
