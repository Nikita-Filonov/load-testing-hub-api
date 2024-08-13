from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from apps.analytics.schema.analytics.number_of_requests_analytics import GetNumberOfRequestsAnalyticsResponse, \
    NumberOfRequestsAnalytics
from apps.analytics.schema.analytics.requests_per_second_analytics import GetRequestsPerSecondAnalyticsResponse, \
    RequestsPerSecondAnalytics
from apps.analytics.schema.analytics.response_times_analytics import GetResponseTimesAnalyticsResponse, \
    ResponseTimesAnalytics
from apps.analytics.schema.methods_analytics import GetMethodsAnalyticsQuery
from services.postgres.models import MethodResultsModel


async def get_analytics_method_results(
        query: GetMethodsAnalyticsQuery,
        session: AsyncSession
) -> Sequence[MethodResultsModel]:
    filters = (
        MethodResultsModel.method == query.method,
        MethodResultsModel.created_at.between(query.start_datetime, query.end_datetime)
    )
    if query.scenario:
        filters += (MethodResultsModel.scenario == query.scenario,)

    return await MethodResultsModel.filter(session, clause_filter=filters)


async def get_methods_number_of_requests_analytics(
        query: GetMethodsAnalyticsQuery,
        session: AsyncSession
) -> GetNumberOfRequestsAnalyticsResponse:
    results = await get_analytics_method_results(query, session)

    return GetNumberOfRequestsAnalyticsResponse(
        analytics=[
            NumberOfRequestsAnalytics(
                datetime=result.created_at,
                number_of_requests=result.number_of_requests,
                number_of_failures=result.number_of_failures
            )
            for result in results
        ]
    )


async def get_methods_requests_per_second_analytics(
        query: GetMethodsAnalyticsQuery,
        session: AsyncSession
) -> GetRequestsPerSecondAnalyticsResponse:
    results = await get_analytics_method_results(query, session)

    return GetRequestsPerSecondAnalyticsResponse(
        analytics=[
            RequestsPerSecondAnalytics(
                datetime=result.created_at,
                requests_per_second=result.requests_per_second,
                failures_per_second=result.failures_per_second
            )
            for result in results
        ]
    )


async def get_methods_response_times_analytics(
        query: GetMethodsAnalyticsQuery,
        session: AsyncSession
) -> GetResponseTimesAnalyticsResponse:
    results = await get_analytics_method_results(query, session)

    return GetResponseTimesAnalyticsResponse(
        analytics=[
            ResponseTimesAnalytics(
                datetime=result.created_at,
                max_response_time=result.max_response_time,
                min_response_time=result.min_response_time,
                average_response_time=result.average_response_time
            )
            for result in results
        ]
    )
