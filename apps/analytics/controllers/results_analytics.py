from apps.analytics.schema.analytics.number_of_requests_analytics import GetNumberOfRequestsAnalyticsResponse, \
    NumberOfRequestsAnalytics
from apps.analytics.schema.analytics.requests_per_second_analytics import GetRequestsPerSecondAnalyticsResponse, \
    RequestsPerSecondAnalytics
from apps.analytics.schema.analytics.response_times_analytics import GetResponseTimesAnalyticsResponse, \
    ResponseTimesAnalytics
from apps.analytics.schema.results_analytics import GetResultsAnalyticsQuery
from services.postgres.repositories.load_test_results import LoadTestResultsRepository


async def get_results_number_of_requests_analytics(
        query: GetResultsAnalyticsQuery,
        load_test_results_repository: LoadTestResultsRepository
) -> GetNumberOfRequestsAnalyticsResponse:
    results = await load_test_results_repository.filter(**query.model_dump())

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
        load_test_results_repository: LoadTestResultsRepository
) -> GetRequestsPerSecondAnalyticsResponse:
    results = await load_test_results_repository.filter(**query.model_dump())

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
        load_test_results_repository: LoadTestResultsRepository
) -> GetResponseTimesAnalyticsResponse:
    results = await load_test_results_repository.filter(**query.model_dump())

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
