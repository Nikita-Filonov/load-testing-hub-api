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
            number_of_users=averages.number_of_users,
            max_response_time=averages.max_response_time,
            min_response_time=averages.min_response_time,
            number_of_requests=averages.number_of_requests,
            number_of_failures=averages.number_of_failures,
            requests_per_second=averages.requests_per_second,
            failures_per_second=averages.failures_per_second,
            median_response_time=averages.median_response_time,
            average_response_time=averages.average_response_time,
            response_time_percentile_50=averages.response_time_percentile_50,
            response_time_percentile_60=averages.response_time_percentile_60,
            response_time_percentile_70=averages.response_time_percentile_70,
            response_time_percentile_80=averages.response_time_percentile_80,
            response_time_percentile_90=averages.response_time_percentile_90,
            response_time_percentile_95=averages.response_time_percentile_95,
            response_time_percentile_99=averages.response_time_percentile_99,
            response_time_percentile_100=averages.response_time_percentile_100,
        )
    )
