from typing import Self, Sequence

from sqlalchemy import Table, ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession

from utils.clients.postgres.base_model import Base
from utils.clients.postgres.types import ColumnExpressionType


class AbstractModel(Base):
    __table__: Table
    __abstract__ = True

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> Self:
        ...

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            clause_filter: ColumnExpressionType,
            **kwargs
    ) -> Self:
        ...

    @classmethod
    async def get(
            cls,
            session: AsyncSession,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> Self | None:
        ...

    @classmethod
    async def filter(
            cls,
            session: AsyncSession,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> Sequence[Self]:
        ...

    @classmethod
    async def count(
            cls,
            session: AsyncSession,
            column: ColumnExpressionArgument,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> int:
        ...

    @classmethod
    async def average(
            cls,
            session: AsyncSession,
            column: ColumnExpressionArgument,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> float:
        ...
