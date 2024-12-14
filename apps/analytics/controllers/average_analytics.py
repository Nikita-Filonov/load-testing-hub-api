from apps.analytics.schema.average_analytics import GetAverageAnalyticsResponse, AverageAnalytics
from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from services.postgres.repositories.load_test_results import LoadTestResultsRepository


async def get_average_analytics(
        query: GetResultsAnalyticsQuery,
        load_test_results_repository: LoadTestResultsRepository
) -> GetAverageAnalyticsResponse:
    averages = await load_test_results_repository.get_averages(**query.model_dump())

    return GetAverageAnalyticsResponse(
        analytics=AverageAnalytics(
            total_requests=averages.total_requests,
            total_failures=averages.total_failures,
            number_of_users=averages.number_of_users,
            max_response_time=averages.max_response_time,
            min_response_time=averages.min_response_time,
            average_response_time=averages.response_time,
            total_requests_per_second=averages.total_requests_per_second,
            total_failures_per_second=averages.total_failures_per_second
        )
    )
