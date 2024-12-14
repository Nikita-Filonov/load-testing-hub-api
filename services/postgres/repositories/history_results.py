from datetime import datetime
from itertools import groupby
from typing import Sequence, Annotated, TypedDict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import HistoryResultsModel
from utils.clients.postgres.repository import BasePostgresRepository


class CreateHistoryResultsModelDict(TypedDict):
    datetime: datetime
    number_of_users: int
    requests_per_second: float
    failures_per_second: float
    load_test_result_id: int
    average_response_time: float
    response_time_percentile_95: float


class HistoryResultsRepository(BasePostgresRepository):
    model = HistoryResultsModel

    async def create_multiple(self, data: list[CreateHistoryResultsModelDict]):
        await self.model.bulk_create(self.session, data)

    async def filter_by_load_test_result_id(self, load_test_result_id: int) -> Sequence[HistoryResultsModel]:
        return await self.model.filter(
            self.session,
            order_by=(self.model.datetime.asc(),),
            clause_filter=(self.model.load_test_result_id == load_test_result_id,)
        )

    async def filter_by_load_test_result_ids_groped(
            self,
            load_test_result_ids: list[int]
    ) -> dict[int, Sequence[HistoryResultsModel]]:
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


async def get_history_results_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> HistoryResultsRepository:
    return HistoryResultsRepository(session=session)
