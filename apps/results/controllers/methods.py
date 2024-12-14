from itertools import zip_longest

from apps.results.schema.methods import MethodDetails, GetMethodDetailsResponse, GetMethodsQuery, \
    GetMethodsResponse, GetShortMethodsQuery, GetShortMethodsResponse, ShortMethod, GetMethodDetailsQuery, Method
from services.postgres.repositories.method_results import MethodResultsRepository


async def get_methods(
        query: GetMethodsQuery,
        method_results_repository: MethodResultsRepository
) -> GetMethodsResponse:
    results = await method_results_repository.filter_with_distinct_by_method(
        method=query.method, service_id=query.service_id, scenario_id=query.scenario_id
    )
    averages = await method_results_repository.get_averages_for_methods(
        methods=[result.method for result in results],
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    return GetMethodsResponse(
        methods=[
            Method(
                method=result.method,
                average_response_time=average.response_time,
                average_number_of_requests=average.number_of_requests,
                average_number_of_failures=average.number_of_failures,
                average_requests_per_second=average.requests_per_second,
            )
            for result, average in zip_longest(results, averages.values())
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
    averages = await method_results_repository.get_averages(**query.model_dump())

    return GetMethodDetailsResponse(
        details=MethodDetails(
            method=query.method,
            average_response_time=averages.response_time,
            average_number_of_requests=averages.number_of_requests,
            average_requests_per_second=averages.requests_per_second,
            average_max_response_time=averages.max_response_time,
            average_min_response_time=averages.min_response_time,
            average_number_of_failures=averages.number_of_failures,
            average_failures_per_second=averages.failures_per_second
        )
    )
