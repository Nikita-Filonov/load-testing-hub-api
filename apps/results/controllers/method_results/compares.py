import asyncio
from itertools import zip_longest
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.load_test_results.details import get_previous_load_test_result
from apps.results.schema.method_results.compares import MethodResultCompare, GetMethodResultsComparesResponse, \
    GetMethodResultsComparesQuery, MethodResultScenarioCompare, GetMethodResultsScenarioComparesQuery, \
    GetMethodResultsScenarioComparesResponse
from services.postgres.models import MethodResultsModel, ScenarioSettingsModel


async def get_method_result_compare(
        session: AsyncSession,
        scenario: str | None,
        result: MethodResultsModel,
        previous_result: MethodResultsModel | None
):
    average_requests_per_second = (
        await MethodResultsModel.get_average_requests_per_second_cached(
            session, result.method, scenario
        )
    )

    previous_requests_per_second: float = 0.0
    if previous_result:
        previous_requests_per_second = previous_result.requests_per_second

    return MethodResultCompare(
        method=result.method,
        current_requests_per_second=result.requests_per_second,
        average_requests_per_second=average_requests_per_second,
        previous_requests_per_second=previous_requests_per_second
    )


async def get_method_results_compares(
        query: GetMethodResultsComparesQuery,
        session: AsyncSession
) -> GetMethodResultsComparesResponse:
    results = await MethodResultsModel.filter(
        session,
        clause_filter=(MethodResultsModel.load_test_results_id == query.load_test_result_id,)
    )

    previous_load_test_result = await get_previous_load_test_result(
        session, query.load_test_result_id, query.service, query.scenario
    )
    previous_results: Sequence[MethodResultsModel] = []
    if previous_load_test_result:
        previous_results = await MethodResultsModel.filter(
            session,
            clause_filter=(MethodResultsModel.load_test_results_id == previous_load_test_result.id,)
        )

    compares: tuple[MethodResultCompare] = await asyncio.gather(*[
        get_method_result_compare(
            session,
            scenario=query.scenario,
            result=result,
            previous_result=previous_result
        )
        for result, previous_result in zip_longest(results, previous_results)
    ])

    return GetMethodResultsComparesResponse(compares=list(compares))


async def get_method_results_scenario_compares(
        query: GetMethodResultsScenarioComparesQuery,
        session: AsyncSession
) -> GetMethodResultsScenarioComparesResponse:
    results = await MethodResultsModel.filter(
        session,
        clause_filter=(MethodResultsModel.load_test_results_id == query.load_test_result_id,)
    )
    settings = await ScenarioSettingsModel.get(
        session, clause_filter=(ScenarioSettingsModel.scenario == query.scenario,)
    )

    compares: list[MethodResultScenarioCompare] = []
    for result in results:
        method_settings = settings.get_method_settings(result.method)

        if method_settings:
            compares.append(MethodResultScenarioCompare(
                method=result.method,
                current_requests_per_second=result.requests_per_second,
                scenario_requests_per_second=method_settings['requests_per_second'],
            ))

    return GetMethodResultsScenarioComparesResponse(compares=compares)
