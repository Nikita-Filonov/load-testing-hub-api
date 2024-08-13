from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.history_results.compares import get_history_results_compare
from apps.results.controllers.history_results.results import get_history_results, create_history_results
from apps.results.schema.history_results.compares import GetHistoryResultsCompareResponse
from apps.results.schema.history_results.results import GetHistoryResultsResponse, GetHistoryResultsQuery, \
    CreateHistoryResultsRequest
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

history_results_router = APIRouter(
    prefix=APIRoutes.HISTORY_RESULTS,
    tags=[APIRoutes.HISTORY_RESULTS.as_tag()]
)


@history_results_router.get('', response_model=GetHistoryResultsResponse)
async def get_history_results_view(
        query: Annotated[GetHistoryResultsQuery, Depends(GetHistoryResultsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_history_results(query, session)


@history_results_router.get('/compare', response_model=GetHistoryResultsCompareResponse)
async def get_history_results_compare_view(
        query: Annotated[GetHistoryResultsQuery, Depends(GetHistoryResultsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_history_results_compare(query, session)


@history_results_router.post('')
async def create_history_results_view(
        request: CreateHistoryResultsRequest,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await create_history_results(request, session)
