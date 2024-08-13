import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from apps.analytics.schema.average_analytics import GetAverageAnalyticsResponse, AverageAnalytics, \
    GetAverageAnalyticsScenarioCompareResponse, AverageAnalyticsScenarioCompare, GetAverageAnalyticsScenarioCompareQuery
from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from services.postgres.models import LoadTestResultsModel, ScenarioSettingsModel


async def get_average_analytics(
        query: GetResultsAnalyticsQuery,
        session: AsyncSession
) -> GetAverageAnalyticsResponse:
    result = await LoadTestResultsModel.get(
        session, clause_filter=(LoadTestResultsModel.service == query.service,)
    )

    average_args = (session, query.scenario, query.end_datetime, query.start_datetime)
    (
        total_requests,
        total_failures,
        number_of_users,
        max_response_time,
        min_response_time,
        average_response_time,
        total_requests_per_second,
        total_failures_per_second
    ) = await asyncio.gather(
        result.get_average_total_requests(*average_args),
        result.get_average_total_failures(*average_args),
        result.get_average_number_of_users(*average_args),
        result.get_average_max_response_time(*average_args),
        result.get_average_min_response_time(*average_args),
        result.get_average_response_time(*average_args),
        result.get_average_total_requests_per_second(*average_args),
        result.get_average_total_failures_per_second(*average_args),
    )

    return GetAverageAnalyticsResponse(
        analytics=AverageAnalytics(
            total_requests=total_requests,
            total_failures=total_failures,
            number_of_users=number_of_users,
            max_response_time=max_response_time,
            min_response_time=min_response_time,
            average_response_time=average_response_time,
            total_requests_per_second=total_requests_per_second,
            total_failures_per_second=total_failures_per_second
        )
    )


async def get_average_analytics_scenario_compare(
        query: GetAverageAnalyticsScenarioCompareQuery,
        session: AsyncSession
) -> GetAverageAnalyticsScenarioCompareResponse:
    result = await LoadTestResultsModel.get(
        session, clause_filter=(LoadTestResultsModel.service == query.service,)
    )
    settings = await ScenarioSettingsModel.get(
        session, clause_filter=(ScenarioSettingsModel.scenario == query.scenario,)
    )

    total_requests_per_second = await result.get_average_total_requests_per_second(
        session, query.scenario, query.end_datetime, query.start_datetime
    )

    return GetAverageAnalyticsScenarioCompareResponse(
        compare=AverageAnalyticsScenarioCompare(
            total_requests_per_second=total_requests_per_second,
            scenario_total_requests_per_second=settings.requests_per_second
        )
    )
