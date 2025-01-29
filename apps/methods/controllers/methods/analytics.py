from apps.analytics.schema.analytics.number_of_requests_analytics import GetNumberOfRequestsAnalyticsResponse, \
    NumberOfRequestsAnalytics
from apps.analytics.schema.analytics.percentiles_analytics import GetPercentilesAnalyticsResponse, PercentilesAnalytics
from apps.analytics.schema.analytics.requests_per_second_analytics import GetRequestsPerSecondAnalyticsResponse, \
    RequestsPerSecondAnalytics
from apps.analytics.schema.analytics.response_times_analytics import GetResponseTimesAnalyticsResponse, \
    ResponseTimesAnalytics
from apps.methods.schema.methods.analytics import GetMethodDetailsAnalyticsQuery
from services.postgres.repositories.method_results import MethodResultsRepository


async def get_method_details_percentiles_analytics(
        query: GetMethodDetailsAnalyticsQuery,
        method_results_repository: MethodResultsRepository
) -> GetPercentilesAnalyticsResponse:
    results = await method_results_repository.filter(
        method=query.method,
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

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


async def get_method_details_number_of_requests_analytics(
        query: GetMethodDetailsAnalyticsQuery,
        method_results_repository: MethodResultsRepository
) -> GetNumberOfRequestsAnalyticsResponse:
    results = await method_results_repository.filter(
        method=query.method,
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

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


async def get_method_details_requests_per_second_analytics(
        query: GetMethodDetailsAnalyticsQuery,
        method_results_repository: MethodResultsRepository
) -> GetRequestsPerSecondAnalyticsResponse:
    results = await method_results_repository.filter(
        method=query.method,
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

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


async def get_method_details_response_times_analytics(
        query: GetMethodDetailsAnalyticsQuery,
        method_results_repository: MethodResultsRepository
) -> GetResponseTimesAnalyticsResponse:
    results = await method_results_repository.filter(
        method=query.method,
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    return GetResponseTimesAnalyticsResponse(
        analytics=[
            ResponseTimesAnalytics(
                datetime=result.created_at,
                max_response_time=result.max_response_time,
                min_response_time=result.min_response_time,
                median_response_time=result.median_response_time,
                average_response_time=result.average_response_time
            )
            for result in results
        ]
    )
