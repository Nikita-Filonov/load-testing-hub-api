from apps.methods.schema.methods.schema import MethodDetails, GetMethodDetailsResponse, GetMethodsQuery, \
    GetMethodsResponse, GetShortMethodsQuery, GetShortMethodsResponse, ShortMethod, GetMethodDetailsQuery, Method
from services.postgres.repositories.method_results import MethodResultsRepository


async def get_methods(
        query: GetMethodsQuery,
        method_results_repository: MethodResultsRepository
) -> GetMethodsResponse:
    results = await method_results_repository.filter_with_distinct_by_method(
        method=query.method,
        protocol=query.protocol,
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

    return GetMethodsResponse(
        methods=[
            Method(
                method=result.method,
                protocol=result.protocol,
                min_response_time=average.min_response_time,
                max_response_time=average.max_response_time,
                number_of_requests=average.number_of_requests,
                number_of_failures=average.number_of_failures,
                requests_per_second=average.requests_per_second,
                failures_per_second=average.failures_per_second,
                median_response_time=average.median_response_time,
                average_response_time=average.average_response_time,
            )
            for result, average in averages.items()
        ]
    )


async def get_short_methods(
        query: GetShortMethodsQuery,
        method_results_repository: MethodResultsRepository
) -> GetShortMethodsResponse:
    results = await method_results_repository.filter_with_distinct_by_method(**query.model_dump())

    return GetShortMethodsResponse(
        methods=[ShortMethod.model_validate(result) for result in results]
    )


async def get_method_details(
        query: GetMethodDetailsQuery,
        method_results_repository: MethodResultsRepository
) -> GetMethodDetailsResponse:
    result = await method_results_repository.get_by_method(method=query.method)
    averages = await method_results_repository.get_averages(**query.model_dump())

    return GetMethodDetailsResponse(
        details=MethodDetails(
            method=result.method,
            protocol=result.protocol,
            max_response_time=averages.max_response_time,
            min_response_time=averages.min_response_time,
            number_of_requests=averages.number_of_requests,
            number_of_failures=averages.number_of_failures,
            requests_per_second=averages.requests_per_second,
            failures_per_second=averages.failures_per_second,
            median_response_time=averages.median_response_time,
            average_response_time=averages.average_response_time,
            average_content_length=averages.average_content_length,
            response_time_percentile_50=averages.response_time_percentile_50,
            response_time_percentile_60=averages.response_time_percentile_60,
            response_time_percentile_70=averages.response_time_percentile_70,
            response_time_percentile_80=averages.response_time_percentile_80,
            response_time_percentile_90=averages.response_time_percentile_90,
            response_time_percentile_95=averages.response_time_percentile_95,
            response_time_percentile_99=averages.response_time_percentile_99,
            response_time_percentile_100=averages.response_time_percentile_100
        )
    )
