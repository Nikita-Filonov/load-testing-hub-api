from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.analytics.controllers.results_analytics import get_results_number_of_requests_analytics, \
    get_results_requests_per_second_analytics, get_results_response_times_analytics
from apps.analytics.schema.analytics.number_of_requests_analytics import GetNumberOfRequestsAnalyticsResponse
from apps.analytics.schema.analytics.requests_per_second_analytics import GetRequestsPerSecondAnalyticsResponse
from apps.analytics.schema.analytics.response_times_analytics import GetResponseTimesAnalyticsResponse
from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

results_analytics_router = APIRouter(
    prefix=APIRoutes.RESULTS_ANALYTICS,
    tags=[APIRoutes.RESULTS_ANALYTICS.as_tag()]
)


@results_analytics_router.get(
    '/number-of-requests',
    response_model=GetNumberOfRequestsAnalyticsResponse
)
async def get_results_number_of_requests_analytics_view(
        query: Annotated[GetResultsAnalyticsQuery, Depends(GetResultsAnalyticsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_results_number_of_requests_analytics(query, session)


@results_analytics_router.get(
    '/requests-per-second',
    response_model=GetRequestsPerSecondAnalyticsResponse
)
async def get_results_requests_per_second_analytics_view(
        query: Annotated[GetResultsAnalyticsQuery, Depends(GetResultsAnalyticsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_results_requests_per_second_analytics(query, session)


@results_analytics_router.get(
    '/response-times',
    response_model=GetResponseTimesAnalyticsResponse
)
async def get_results_response_times_analytics_view(
        query: Annotated[GetResultsAnalyticsQuery, Depends(GetResultsAnalyticsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_results_response_times_analytics(query, session)
