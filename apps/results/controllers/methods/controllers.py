import asyncio
from typing import Sequence

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.methods.schema import MethodDetails, GetMethodDetailsResponse, GetMethodsQuery, \
    GetMethodsResponse, GetShortMethodsQuery, GetShortMethodsResponse, ShortMethod, GetMethodDetailsQuery, Method
from services.postgres.models import MethodResultsModel


async def get_methods_with_filters(
        query: GetMethodsQuery,
        session: AsyncSession
) -> Sequence[MethodResultsModel]:
    filters = (MethodResultsModel.service == query.service,)
    if query.method:
        filters += (func.lower(MethodResultsModel.method).contains(query.method.lower()),)

    if query.scenario:
        filters += (MethodResultsModel.scenario == query.scenario,)

    results = await MethodResultsModel.filter(
        session,
        distinct=(MethodResultsModel.method,),
        clause_filter=filters
    )

    return results


async def get_methods(query: GetMethodsQuery, session: AsyncSession) -> GetMethodsResponse:
    results = await get_methods_with_filters(query, session)

    methods: list[Method] = []
    average_args = (session, query.scenario, query.end_datetime, query.start_datetime)
    for result in results:
        (response_time, number_of_requests, number_of_failures, requests_per_second) = await asyncio.gather(
            result.get_average_response_time(*average_args),
            result.get_average_number_of_requests(*average_args),
            result.get_average_number_of_failures(*average_args),
            result.get_average_requests_per_second(*average_args),
        )

        methods.append(
            Method(
                method=result.method,
                service=result.service,
                average_response_time=response_time,
                average_number_of_requests=number_of_requests,
                average_number_of_failures=number_of_failures,
                average_requests_per_second=requests_per_second,
            )
        )

    return GetMethodsResponse(methods=methods)


async def get_short_methods(
        query: GetShortMethodsQuery,
        session: AsyncSession
) -> GetShortMethodsResponse:
    methods_query = GetMethodsQuery(**query.model_dump())
    results = await get_methods_with_filters(methods_query, session)

    return GetShortMethodsResponse(
        methods=[ShortMethod.model_validate(result) for result in results]
    )


async def get_method_details(
        query: GetMethodDetailsQuery,
        session: AsyncSession
) -> GetMethodDetailsResponse:
    result = await MethodResultsModel.get(
        session,
        clause_filter=(MethodResultsModel.method == query.method,)
    )

    average_args = (session, query.scenario, query.end_datetime, query.start_datetime)
    (
        response_time,
        min_response_time,
        max_response_time,
        number_of_requests,
        number_of_failures,
        requests_per_second,
        failures_per_second
    ) = await asyncio.gather(
        result.get_average_response_time(*average_args),
        result.get_average_min_response_time(*average_args),
        result.get_average_max_response_time(*average_args),
        result.get_average_number_of_requests(*average_args),
        result.get_average_number_of_failures(*average_args),
        result.get_average_requests_per_second(*average_args),
        result.get_average_failures_per_second(*average_args),
    )

    return GetMethodDetailsResponse(
        details=MethodDetails(
            method=result.method,
            service=result.service,
            average_response_time=response_time,
            average_number_of_requests=number_of_requests,
            average_requests_per_second=requests_per_second,
            average_max_response_time=max_response_time,
            average_min_response_time=min_response_time,
            average_number_of_failures=number_of_failures,
            average_failures_per_second=failures_per_second
        )
    )
