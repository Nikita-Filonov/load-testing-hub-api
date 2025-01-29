from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.method_results_history import get_method_results_history, create_method_results_history
from apps.results.schema.results_history.base import GetResultsHistoryResponse
from apps.results.schema.results_history.method_results_history import CreateMethodResultsHistoryRequest, \
    GetMethodResultsHistoryQuery
from services.postgres.repositories.method_results_history import MethodResultsHistoryRepository, \
    get_method_results_history_repository
from utils.routes import APIRoutes

method_results_history_router = APIRouter(
    prefix=APIRoutes.METHOD_RESULTS_HISTORY,
    tags=[APIRoutes.METHOD_RESULTS_HISTORY.as_tag()]
)


@method_results_history_router.get('', response_model=GetResultsHistoryResponse)
async def get_method_results_history_view(
        query: Annotated[GetMethodResultsHistoryQuery, Depends(GetMethodResultsHistoryQuery.as_query)],
        method_results_history_repository: Annotated[
            MethodResultsHistoryRepository, Depends(get_method_results_history_repository)
        ],
):
    return await get_method_results_history(query, method_results_history_repository)


@method_results_history_router.post('')
async def create_method_results_history_view(
        request: CreateMethodResultsHistoryRequest,
        method_results_history_repository: Annotated[
            MethodResultsHistoryRepository, Depends(get_method_results_history_repository)
        ],
):
    return await create_method_results_history(request, method_results_history_repository)
