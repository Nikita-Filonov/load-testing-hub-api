from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.history_results.results import GetHistoryResultsResponse, GetHistoryResultsQuery, \
    HistoryResult, \
    CreateHistoryResultsRequest
from services.postgres.models import HistoryResultsModel


async def get_history_results_with_filters(
        query: GetHistoryResultsQuery,
        session: AsyncSession
) -> Sequence[HistoryResultsModel]:
    return await HistoryResultsModel.filter(
        session,
        order_by=(HistoryResultsModel.datetime.asc(),),
        clause_filter=(HistoryResultsModel.load_test_results_id == query.load_test_result_id,)
    )


async def get_history_results(
        query: GetHistoryResultsQuery,
        session: AsyncSession
) -> GetHistoryResultsResponse:
    results = await get_history_results_with_filters(query, session)

    return GetHistoryResultsResponse(
        results=[HistoryResult.model_validate(result) for result in results]
    )


async def create_history_results(request: CreateHistoryResultsRequest, session: AsyncSession):
    for result in request.results:
        await HistoryResultsModel.create(
            session, **result.model_dump(), load_test_results_id=request.load_test_results_id
        )
