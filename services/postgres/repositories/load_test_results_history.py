from itertools import groupby
from typing import Sequence, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import LoadTestResultsHistoryModel
from services.postgres.models.base.content_length import ContentLengthModelDict
from services.postgres.models.base.datetime import DatetimeModelDict
from services.postgres.models.base.metrics import MetricsModelDict
from services.postgres.models.base.number_of_users import NumberOfUsersModelDict
from utils.clients.postgres.repository import BasePostgresRepository


class CreateLoadTestResultsHistoryModelDict(
    MetricsModelDict,
    DatetimeModelDict,
    NumberOfUsersModelDict,
    ContentLengthModelDict
):
    load_test_result_id: int


class LoadTestResultsHistoryRepository(BasePostgresRepository):
    model = LoadTestResultsHistoryModel

    async def create_multiple(self, data: list[CreateLoadTestResultsHistoryModelDict]):
        await self.model.bulk_create(self.session, data)

    async def filter_by_load_test_result_id(
            self,
            load_test_result_id: int
    ) -> Sequence[LoadTestResultsHistoryModel]:
        return await self.model.filter(
            self.session,
            order_by=(self.model.datetime.asc(),),
            clause_filter=(self.model.load_test_result_id == load_test_result_id,)
        )

    async def filter_by_load_test_result_ids_groped(
            self,
            load_test_result_ids: list[int]
    ) -> dict[int, Sequence[LoadTestResultsHistoryModel]]:
        results = await self.model.filter(
            self.session,
            order_by=(
                self.model.load_test_result_id.asc(),
                self.model.datetime.asc()
            ),
            clause_filter=(self.model.load_test_result_id.in_(load_test_result_ids),)
        )

        return {
            load_test_result_id: list(results)
            for load_test_result_id, results
            in groupby(results, key=lambda r: r.load_test_result_id)
        }


async def get_load_test_results_history_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> LoadTestResultsHistoryRepository:
    return LoadTestResultsHistoryRepository(session=session)
