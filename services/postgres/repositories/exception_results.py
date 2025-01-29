from typing import Sequence, Annotated, TypedDict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import ExceptionResultsModel
from utils.clients.postgres.repository import BasePostgresRepository


class CreateExceptionResultsModelDict(TypedDict):
    message: str
    details: str
    load_test_result_id: int
    number_of_exceptions: int


class ExceptionResultsRepository(BasePostgresRepository):
    model = ExceptionResultsModel

    async def get_by_id(self, exception_result_id: int) -> ExceptionResultsModel | None:
        return await self.model.get(
            self.session, clause_filter=(self.model.id == exception_result_id,)
        )

    async def filter_by_load_test_result_id(
            self,
            load_test_result_id: int
    ) -> Sequence[ExceptionResultsModel]:
        return await self.model.filter(
            self.session, clause_filter=(self.model.load_test_result_id == load_test_result_id,)
        )

    async def create_multiple(self, data: list[CreateExceptionResultsModelDict]):
        await self.model.bulk_create(self.session, data)


async def get_exception_results_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> ExceptionResultsRepository:
    return ExceptionResultsRepository(session=session)
