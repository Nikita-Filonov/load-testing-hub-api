from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.load_test_results_history import get_load_test_results_history, \
    create_load_test_results_history
from apps.results.schema.results_history.base import GetResultsHistoryResponse
from apps.results.schema.results_history.load_test_results_history import GetLoadTestResultsHistoryQuery, \
    CreateLoadTestResultsHistoryRequest
from services.postgres.repositories.load_test_results_history import LoadTestResultsHistoryRepository, \
    get_load_test_results_history_repository
from utils.routes import APIRoutes

load_test_results_history_router = APIRouter(
    prefix=APIRoutes.LOAD_TEST_RESULTS_HISTORY,
    tags=[APIRoutes.LOAD_TEST_RESULTS_HISTORY.as_tag()]
)


@load_test_results_history_router.get('', response_model=GetResultsHistoryResponse)
async def get_load_test_results_history_view(
        query: Annotated[GetLoadTestResultsHistoryQuery, Depends(GetLoadTestResultsHistoryQuery.as_query)],
        load_test_results_history_repository: Annotated[
            LoadTestResultsHistoryRepository, Depends(get_load_test_results_history_repository)
        ],
):
    return await get_load_test_results_history(query, load_test_results_history_repository)


@load_test_results_history_router.post('')
async def create_load_test_results_history_view(
        request: CreateLoadTestResultsHistoryRequest,
        load_test_results_history_repository: Annotated[
            LoadTestResultsHistoryRepository, Depends(get_load_test_results_history_repository)
        ],
):
    return await create_load_test_results_history(request, load_test_results_history_repository)
