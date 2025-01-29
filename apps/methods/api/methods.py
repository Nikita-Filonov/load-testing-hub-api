from typing import Annotated

from fastapi import APIRouter, Depends

from apps.analytics.schema.analytics.number_of_requests_analytics import GetNumberOfRequestsAnalyticsResponse
from apps.analytics.schema.analytics.percentiles_analytics import GetPercentilesAnalyticsResponse
from apps.analytics.schema.analytics.requests_per_second_analytics import GetRequestsPerSecondAnalyticsResponse
from apps.analytics.schema.analytics.response_times_analytics import GetResponseTimesAnalyticsResponse
from apps.methods.controllers.methods.analytics import get_method_details_percentiles_analytics, \
    get_method_details_response_times_analytics, get_method_details_requests_per_second_analytics, \
    get_method_details_number_of_requests_analytics
from apps.methods.controllers.methods.controllers import get_methods, get_short_methods, get_method_details
from apps.methods.schema.methods.analytics import GetMethodDetailsAnalyticsQuery
from apps.methods.schema.methods.schema import GetMethodsQuery, GetMethodsResponse, GetShortMethodsResponse, \
    GetShortMethodsQuery, GetMethodDetailsQuery, GetMethodDetailsResponse
from services.postgres.repositories.method_results import MethodResultsRepository, get_method_results_repository
from utils.routes import APIRoutes

methods_router = APIRouter(
    prefix=APIRoutes.METHODS,
    tags=[APIRoutes.METHODS.as_tag()]
)


@methods_router.get('', response_model=GetMethodsResponse)
async def get_methods_view(
        query: Annotated[GetMethodsQuery, Depends(GetMethodsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_methods(query, method_results_repository)


@methods_router.get('/short', response_model=GetShortMethodsResponse)
async def get_short_methods_view(
        query: Annotated[GetShortMethodsQuery, Depends(GetShortMethodsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_short_methods(query, method_results_repository)


@methods_router.get('/details', response_model=GetMethodDetailsResponse)
async def get_method_details_view(
        query: Annotated[GetMethodDetailsQuery, Depends(GetMethodDetailsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_method_details(query, method_results_repository)


@methods_router.get('/details-percentiles-analytics', response_model=GetPercentilesAnalyticsResponse)
async def get_method_details_percentiles_analytics_view(
        query: Annotated[GetMethodDetailsAnalyticsQuery, Depends(GetMethodDetailsAnalyticsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_method_details_percentiles_analytics(query, method_results_repository)


@methods_router.get('/details-response-times-analytics', response_model=GetResponseTimesAnalyticsResponse)
async def get_method_details_response_times_analytics_view(
        query: Annotated[GetMethodDetailsAnalyticsQuery, Depends(GetMethodDetailsAnalyticsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_method_details_response_times_analytics(query, method_results_repository)


@methods_router.get(
    '/details-number-of-requests-analytics',
    response_model=GetNumberOfRequestsAnalyticsResponse
)
async def get_method_details_number_of_requests_analytics_view(
        query: Annotated[GetMethodDetailsAnalyticsQuery, Depends(GetMethodDetailsAnalyticsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_method_details_number_of_requests_analytics(query, method_results_repository)


@methods_router.get(
    '/details-requests-per-second-analytics',
    response_model=GetRequestsPerSecondAnalyticsResponse
)
async def get_method_details_requests_per_second_analytics_view(
        query: Annotated[GetMethodDetailsAnalyticsQuery, Depends(GetMethodDetailsAnalyticsQuery.as_query)],
        method_results_repository: Annotated[MethodResultsRepository, Depends(get_method_results_repository)]
):
    return await get_method_details_requests_per_second_analytics(query, method_results_repository)
