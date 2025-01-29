from apps.analytics.schema.analytics.number_of_requests_analytics import GetNumberOfRequestsAnalyticsResponse, \
    NumberOfRequestsAnalytics
from apps.analytics.schema.analytics.percentiles_analytics import GetPercentilesAnalyticsResponse, PercentilesAnalytics
from apps.analytics.schema.analytics.requests_per_second_analytics import GetRequestsPerSecondAnalyticsResponse, \
    RequestsPerSecondAnalytics
from apps.analytics.schema.analytics.response_times_analytics import GetResponseTimesAnalyticsResponse, \
    ResponseTimesAnalytics
from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from services.postgres.repositories.load_test_results import LoadTestResultsRepository


async def get_results_percentiles_analytics(
        query: GetResultsAnalyticsQuery,
        load_test_results_repository: LoadTestResultsRepository
) -> GetPercentilesAnalyticsResponse:
    results = await load_test_results_repository.filter(**query.model_dump())

    return GetPercentilesAnalyticsResponse(
        analytics=[
            PercentilesAnalytics(
                datetime=result.created_at,
                response_time_percentile_50=result.response_time_percentile_50,
                response_time_percentile_60=result.response_time_percentile_60,
                response_time_percentile_70=result.response_time_percentile_70,
                response_time_percentile_80=result.response_time_percentile_80,
                response_time_percentile_90=result.response_time_percentile_90,
                response_time_percentile_95=result.response_time_percentile_95,
                response_time_percentile_99=result.response_time_percentile_99,
                response_time_percentile_100=result.response_time_percentile_100,
            )
            for result in results
        ]
    )


async def get_results_number_of_requests_analytics(
        query: GetResultsAnalyticsQuery,
        load_test_results_repository: LoadTestResultsRepository
) -> GetNumberOfRequestsAnalyticsResponse:
    results = await load_test_results_repository.filter(**query.model_dump())

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


async def get_results_requests_per_second_analytics(
        query: GetResultsAnalyticsQuery,
        load_test_results_repository: LoadTestResultsRepository
) -> GetRequestsPerSecondAnalyticsResponse:
    results = await load_test_results_repository.filter(**query.model_dump())

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


async def get_results_response_times_analytics(
        query: GetResultsAnalyticsQuery,
        load_test_results_repository: LoadTestResultsRepository
) -> GetResponseTimesAnalyticsResponse:
    results = await load_test_results_repository.filter(**query.model_dump())

    return GetResponseTimesAnalyticsResponse(
        analytics=[
            ResponseTimesAnalytics(
                datetime=result.created_at,
                min_response_time=result.min_response_time,
                max_response_time=result.max_response_time,
                median_response_time=result.median_response_time,
                average_response_time=result.average_response_time
            )
            for result in results
        ]
    )
