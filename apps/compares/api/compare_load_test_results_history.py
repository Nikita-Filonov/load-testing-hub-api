from typing import Annotated

from fastapi import APIRouter, Depends

from apps.compares.controllers.compares.compare_results_history.compare_load_test_results_history import \
    get_compare_load_test_results_history_response_times, get_compare_load_test_results_history_requests_per_second, \
    get_compare_load_test_results_history_number_of_requests, get_compare_load_test_results_history_number_of_users
from apps.compares.schema.compares.compare_results_history.base import \
    GetCompareResultsHistoryRequestsPerSecondResponse, GetCompareResultsHistoryNumberOfRequestsResponse, \
    GetCompareResultsHistoryNumberOfUsersResponse, GetCompareResultsHistoryResponseTimesResponse
from apps.compares.schema.compares.compare_results_history.compare_load_test_results_history import \
    GetCompareLoadTestResultsHistoryQuery
from services.postgres.repositories.load_test_results import LoadTestResultsRepository, get_load_test_results_repository
from services.postgres.repositories.load_test_results_history import LoadTestResultsHistoryRepository, \
    get_load_test_results_history_repository
from utils.routes import APIRoutes

compare_load_test_results_history_router = APIRouter(
    prefix=APIRoutes.COMPARES,
    tags=[APIRoutes.COMPARES.as_tag()]
)


@compare_load_test_results_history_router.get(
    '/compare-load-test-results-history-response-times',
    response_model=GetCompareResultsHistoryResponseTimesResponse
)
async def get_compare_load_test_results_history_response_times_view(
        query: Annotated[
            GetCompareLoadTestResultsHistoryQuery, Depends(GetCompareLoadTestResultsHistoryQuery.as_query)
        ],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
        load_test_results_history_repository: Annotated[
            LoadTestResultsHistoryRepository, Depends(get_load_test_results_history_repository)
        ],
):
    return await get_compare_load_test_results_history_response_times(
        query,
        load_test_results_repository=load_test_results_repository,
        load_test_results_history_repository=load_test_results_history_repository,
    )


@compare_load_test_results_history_router.get(
    '/compare-load-test-results-history-number-of-users',
    response_model=GetCompareResultsHistoryNumberOfUsersResponse
)
async def get_compare_load_test_results_history_number_of_users_view(
        query: Annotated[
            GetCompareLoadTestResultsHistoryQuery, Depends(GetCompareLoadTestResultsHistoryQuery.as_query)
        ],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
        load_test_results_history_repository: Annotated[
            LoadTestResultsHistoryRepository, Depends(get_load_test_results_history_repository)
        ],
):
    return await get_compare_load_test_results_history_number_of_users(
        query,
        load_test_results_repository=load_test_results_repository,
        load_test_results_history_repository=load_test_results_history_repository,
    )


@compare_load_test_results_history_router.get(
    '/compare-load-test-results-history-number-of-requests',
    response_model=GetCompareResultsHistoryNumberOfRequestsResponse
)
async def get_compare_load_test_results_history_number_of_requests_view(
        query: Annotated[
            GetCompareLoadTestResultsHistoryQuery, Depends(GetCompareLoadTestResultsHistoryQuery.as_query)
        ],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
        load_test_results_history_repository: Annotated[
            LoadTestResultsHistoryRepository, Depends(get_load_test_results_history_repository)
        ],
):
    return await get_compare_load_test_results_history_number_of_requests(
        query,
        load_test_results_repository=load_test_results_repository,
        load_test_results_history_repository=load_test_results_history_repository,
    )


@compare_load_test_results_history_router.get(
    '/compare-load-test-results-history-requests-per-second',
    response_model=GetCompareResultsHistoryRequestsPerSecondResponse
)
async def get_compare_load_test_results_history_requests_per_second_view(
        query: Annotated[
            GetCompareLoadTestResultsHistoryQuery, Depends(GetCompareLoadTestResultsHistoryQuery.as_query)
        ],
        load_test_results_repository: Annotated[LoadTestResultsRepository, Depends(get_load_test_results_repository)],
        load_test_results_history_repository: Annotated[
            LoadTestResultsHistoryRepository, Depends(get_load_test_results_history_repository)
        ],
):
    return await get_compare_load_test_results_history_requests_per_second(
        query,
        load_test_results_repository=load_test_results_repository,
        load_test_results_history_repository=load_test_results_history_repository,
    )
