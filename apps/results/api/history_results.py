from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.history_results import get_history_results, create_history_results
from apps.results.schema.history_results import GetHistoryResultsResponse, GetHistoryResultsQuery, \
    CreateHistoryResultsRequest
from services.postgres.repositories.history_results import HistoryResultsRepository, get_history_results_repository
from utils.routes import APIRoutes

history_results_router = APIRouter(
    prefix=APIRoutes.HISTORY_RESULTS,
    tags=[APIRoutes.HISTORY_RESULTS.as_tag()]
)


@history_results_router.get('', response_model=GetHistoryResultsResponse)
async def get_history_results_view(
        query: Annotated[GetHistoryResultsQuery, Depends(GetHistoryResultsQuery.as_query)],
        history_results_repository: Annotated[HistoryResultsRepository, Depends(get_history_results_repository)],
):
    return await get_history_results(query, history_results_repository)


@history_results_router.post('')
async def create_history_results_view(
        request: CreateHistoryResultsRequest,
        history_results_repository: Annotated[HistoryResultsRepository, Depends(get_history_results_repository)],
):
    return await create_history_results(request, history_results_repository)
