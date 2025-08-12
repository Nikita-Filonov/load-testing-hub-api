from apps.analytics.schema.methods_analytics import GetMethodsAnalyticsQuery, \
    GetMethodsRequestsPerSecondAnalyticsResponse, MethodsRequestsPerSecondAnalytics, \
    GetMethodsNumberOfRequestsAnalyticsResponse, MethodsNumberOfRequestsAnalytics, \
    GetMethodsResponseTimesAnalyticsResponse, MethodsResponseTimesAnalytics
from services.postgres.repositories.method_results import MethodResultsRepository


async def get_methods_number_of_requests_analytics(
        query: GetMethodsAnalyticsQuery,
        method_results_repository: MethodResultsRepository
) -> GetMethodsNumberOfRequestsAnalyticsResponse:
    results = await method_results_repository.filter_with_distinct_by_method(
        service_id=query.service_id,
        scenario_id=query.scenario_id
    )
    averages = await method_results_repository.get_averages_for_method_results(
        results=results,
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    return GetMethodsNumberOfRequestsAnalyticsResponse(
        analytics=[
            MethodsNumberOfRequestsAnalytics(
                method=result.method,
                protocol=result.protocol,
                number_of_requests=average.number_of_requests,
                number_of_failures=average.number_of_failures
            )
            for result, average in averages.items()
        ]
    )


async def get_methods_requests_per_second_analytics(
        query: GetMethodsAnalyticsQuery,
        method_results_repository: MethodResultsRepository
) -> GetMethodsRequestsPerSecondAnalyticsResponse:
    results = await method_results_repository.filter_with_distinct_by_method(
        service_id=query.service_id,
        scenario_id=query.scenario_id
    )
    averages = await method_results_repository.get_averages_for_method_results(
        results=results,
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    return GetMethodsRequestsPerSecondAnalyticsResponse(
        analytics=[
            MethodsRequestsPerSecondAnalytics(
                method=result.method,
                protocol=result.protocol,
                requests_per_second=average.requests_per_second,
                failures_per_second=average.failures_per_second,
            )
            for result, average in averages.items()
        ]
    )


async def get_methods_response_times_analytics(
        query: GetMethodsAnalyticsQuery,
        method_results_repository: MethodResultsRepository
) -> GetMethodsResponseTimesAnalyticsResponse:
    results = await method_results_repository.filter_with_distinct_by_method(
        service_id=query.service_id, scenario_id=query.scenario_id
    )
    averages = await method_results_repository.get_averages_for_method_results(
        results=results,
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    return GetMethodsResponseTimesAnalyticsResponse(
        analytics=[
            MethodsResponseTimesAnalytics(
                method=result.method,
                protocol=result.protocol,
                max_response_time=average.max_response_time,
                min_response_time=average.min_response_time,
                median_response_time=average.median_response_time,
                average_response_time=average.average_response_time
            )
            for result, average in averages.items()
        ]
    )
