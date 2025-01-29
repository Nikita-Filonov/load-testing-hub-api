from typing import Annotated

from fastapi import APIRouter, Depends

from apps.compares.controllers.compares.compare_results_history.compare_method_results_history import \
    get_compare_method_results_history_response_times, get_compare_method_results_history_requests_per_second, \
    get_compare_method_results_history_number_of_requests, get_compare_method_results_history_number_of_users
from apps.compares.schema.compares.compare_results_history.base import \
    GetCompareResultsHistoryRequestsPerSecondResponse, GetCompareResultsHistoryNumberOfRequestsResponse, \
    GetCompareResultsHistoryNumberOfUsersResponse, GetCompareResultsHistoryResponseTimesResponse
from apps.compares.schema.compares.compare_results_history.compare_method_results_history import \
    GetCompareMethodResultsHistoryQuery
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from services.postgres.repositories.method_results_history import MethodResultsHistoryRepository, \
    get_method_results_history_repository
from utils.routes import APIRoutes

compare_method_results_history_router = APIRouter(
    prefix=APIRoutes.COMPARES,
    tags=[APIRoutes.COMPARES.as_tag()]
)


@compare_method_results_history_router.get(
    '/compare-method-results-history-response-times',
    response_model=GetCompareResultsHistoryResponseTimesResponse
)
async def get_compare_method_results_history_response_times_view(
        query: Annotated[GetCompareMethodResultsHistoryQuery, Depends(GetCompareMethodResultsHistoryQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        method_results_history_repository: Annotated[
            MethodResultsHistoryRepository, Depends(get_method_results_history_repository)
        ],
):
    return await get_compare_method_results_history_response_times(
        query,
        method_results_repository=method_results_repository,
        method_results_history_repository=method_results_history_repository,
    )


@compare_method_results_history_router.get(
    '/compare-method-results-history-number-of-users',
    response_model=GetCompareResultsHistoryNumberOfUsersResponse
)
async def get_compare_method_results_history_number_of_users_view(
        query: Annotated[GetCompareMethodResultsHistoryQuery, Depends(GetCompareMethodResultsHistoryQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        method_results_history_repository: Annotated[
            MethodResultsHistoryRepository, Depends(get_method_results_history_repository)
        ],
):
    return await get_compare_method_results_history_number_of_users(
        query,
        method_results_repository=method_results_repository,
        method_results_history_repository=method_results_history_repository,
    )


@compare_method_results_history_router.get(
    '/compare-method-results-history-number-of-requests',
    response_model=GetCompareResultsHistoryNumberOfRequestsResponse
)
async def get_compare_method_results_history_number_of_requests_view(
        query: Annotated[GetCompareMethodResultsHistoryQuery, Depends(GetCompareMethodResultsHistoryQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        method_results_history_repository: Annotated[
            MethodResultsHistoryRepository, Depends(get_method_results_history_repository)
        ],
):
    return await get_compare_method_results_history_number_of_requests(
        query,
        method_results_repository=method_results_repository,
        method_results_history_repository=method_results_history_repository,
    )


@compare_method_results_history_router.get(
    '/compare-method-results-history-requests-per-second',
    response_model=GetCompareResultsHistoryRequestsPerSecondResponse
)
async def get_compare_method_results_history_requests_per_second_view(
        query: Annotated[GetCompareMethodResultsHistoryQuery, Depends(GetCompareMethodResultsHistoryQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)],
        method_results_history_repository: Annotated[
            MethodResultsHistoryRepository, Depends(get_method_results_history_repository)
        ],
):
    return await get_compare_method_results_history_requests_per_second(
        query,
        method_results_repository=method_results_repository,
        method_results_history_repository=method_results_history_repository,
    )
