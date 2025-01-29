from typing import Annotated

from fastapi import APIRouter, Depends

from apps.analytics.controllers.methods_analytics import get_methods_number_of_requests_analytics, \
    get_methods_requests_per_second_analytics, get_methods_response_times_analytics
from apps.analytics.schema.methods_analytics import GetMethodsAnalyticsQuery, GetMethodsResponseTimesAnalyticsResponse, \
    GetMethodsRequestsPerSecondAnalyticsResponse, GetMethodsNumberOfRequestsAnalyticsResponse
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from utils.routes import APIRoutes

methods_analytics_router = APIRouter(
    prefix=APIRoutes.METHODS_ANALYTICS,
    tags=[APIRoutes.METHODS_ANALYTICS.as_tag()]
)


@methods_analytics_router.get(
    '/number-of-requests',
    response_model=GetMethodsNumberOfRequestsAnalyticsResponse
)
async def get_methods_number_of_requests_analytics_view(
        query: Annotated[GetMethodsAnalyticsQuery, Depends(GetMethodsAnalyticsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_methods_number_of_requests_analytics(query, method_results_repository)


@methods_analytics_router.get(
    '/requests-per-second',
    response_model=GetMethodsRequestsPerSecondAnalyticsResponse
)
async def get_methods_requests_per_second_analytics_view(
        query: Annotated[GetMethodsAnalyticsQuery, Depends(GetMethodsAnalyticsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_methods_requests_per_second_analytics(query, method_results_repository)


@methods_analytics_router.get(
    '/response-times',
    response_model=GetMethodsResponseTimesAnalyticsResponse
)
async def get_methods_response_times_analytics_view(
        query: Annotated[GetMethodsAnalyticsQuery, Depends(GetMethodsAnalyticsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_methods_response_times_analytics(query, method_results_repository)
