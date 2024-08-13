from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from apps.analytics.schema.analytics.number_of_requests_analytics import GetNumberOfRequestsAnalyticsResponse, \
    NumberOfRequestsAnalytics
from apps.analytics.schema.analytics.requests_per_second_analytics import GetRequestsPerSecondAnalyticsResponse, \
    RequestsPerSecondAnalytics
from apps.analytics.schema.analytics.response_times_analytics import GetResponseTimesAnalyticsResponse, \
    ResponseTimesAnalytics
from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from services.postgres.models import LoadTestResultsModel


async def get_analytics_load_test_results(
        query: GetResultsAnalyticsQuery,
        session: AsyncSession
) -> Sequence[LoadTestResultsModel]:
    filters = (
        LoadTestResultsModel.service == query.service,
        LoadTestResultsModel.created_at.between(query.start_datetime, query.end_datetime)
    )
    if query.scenario:
        filters += (LoadTestResultsModel.scenario == query.scenario,)

    return await LoadTestResultsModel.filter(session, clause_filter=filters)


async def get_results_number_of_requests_analytics(
        query: GetResultsAnalyticsQuery,
        session: AsyncSession
) -> GetNumberOfRequestsAnalyticsResponse:
    results = await get_analytics_load_test_results(query, session)

    return GetNumberOfRequestsAnalyticsResponse(
        analytics=[
            NumberOfRequestsAnalytics(
                datetime=result.created_at,
                number_of_requests=result.total_requests,
                number_of_failures=result.total_failures
            )
            for result in results
        ]
    )


async def get_results_requests_per_second_analytics(
        query: GetResultsAnalyticsQuery,
        session: AsyncSession
) -> GetRequestsPerSecondAnalyticsResponse:
    results = await get_analytics_load_test_results(query, session)

    return GetRequestsPerSecondAnalyticsResponse(
        analytics=[
            RequestsPerSecondAnalytics(
                datetime=result.created_at,
                requests_per_second=result.total_requests_per_second,
                failures_per_second=result.total_failures_per_second
            )
            for result in results
        ]
    )


async def get_results_response_times_analytics(
        query: GetResultsAnalyticsQuery,
        session: AsyncSession
) -> GetResponseTimesAnalyticsResponse:
    results = await get_analytics_load_test_results(query, session)

    return GetResponseTimesAnalyticsResponse(
        analytics=[
            ResponseTimesAnalytics(
                datetime=result.created_at,
                min_response_time=result.min_response_time,
                max_response_time=result.max_response_time,
                average_response_time=result.average_response_time
            )
            for result in results
        ]
    )
