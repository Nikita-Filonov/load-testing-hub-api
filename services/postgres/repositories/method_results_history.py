from itertools import groupby
from typing import Sequence, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import MethodResultsHistoryModel
from services.postgres.models.base.content_length import ContentLengthModelDict
from services.postgres.models.base.datetime import DatetimeModelDict
from services.postgres.models.base.metrics import MetricsModelDict
from services.postgres.models.base.number_of_users import NumberOfUsersModelDict
from utils.clients.postgres.repository import BasePostgresRepository


class CreateMethodResultsHistoryModelDict(
    MetricsModelDict,
    DatetimeModelDict,
    NumberOfUsersModelDict,
    ContentLengthModelDict
):
    method_result_id: int


class MethodResultsHistoryRepository(BasePostgresRepository):
    model = MethodResultsHistoryModel

    async def create_multiple(self, data: list[CreateMethodResultsHistoryModelDict]):
        await self.model.bulk_create(self.session, data)

    async def filter_by_method_result_id(self, method_result_id: int) -> Sequence[MethodResultsHistoryModel]:
        return await self.model.filter(
            self.session,
            order_by=(self.model.datetime.asc(),),
            clause_filter=(self.model.method_result_id == method_result_id,)
        )

    async def filter_by_method_result_ids_groped(
            self,
            method_result_ids: list[int]
    ) -> dict[int, Sequence[MethodResultsHistoryModel]]:
        results = await self.model.filter(
            self.session,
            order_by=(
                self.model.method_result_id.asc(),
                self.model.datetime.asc()
            ),
            clause_filter=(self.model.method_result_id.in_(method_result_ids),)
        )

        return {
            method_result_id: list(results)
            for method_result_id, results
            in groupby(results, key=lambda r: r.method_result_id)
        }


async def get_method_results_history_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> MethodResultsHistoryRepository:
    return MethodResultsHistoryRepository(session=session)
