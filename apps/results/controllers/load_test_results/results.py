from typing import Sequence

from apps.results.controllers.load_test_results.compares import get_load_test_result_summary_compare
from apps.results.schema.load_test_results.compares import LoadTestResultSummaryCompare
from apps.results.schema.load_test_results.results import GetLoadTestResultsQuery, \
    GetLoadTestResultsResponse, LoadTestResult
from services.postgres.models.load_test_results import LoadTestResultsModel
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository


async def get_load_test_results_compares(
        query: GetLoadTestResultsQuery,
        results: Sequence[LoadTestResultsModel],
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> list[LoadTestResultSummaryCompare]:
    compare_settings = await compare_settings_repository.get_or_create(query.service_id)
    load_test_result_averages = await load_test_results_repository.get_averages(
        service_id=query.service_id, scenario_id=query.scenario_id
    )

    return [
        get_load_test_result_summary_compare(
            result=result,
            previous_result=results[index + 1] if (index + 1) < len(results) else None,
            compare_settings=compare_settings,
            load_test_result_averages=load_test_result_averages
        )
        for index, result in enumerate(results)
    ]


def get_load_test_result_with_compare(
        result: LoadTestResultsModel,
        compare: LoadTestResultSummaryCompare
) -> LoadTestResult:
    load_test_result = LoadTestResult.model_validate(result)
    load_test_result.compare = compare

    return load_test_result


async def get_load_test_results(
        query: GetLoadTestResultsQuery,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> GetLoadTestResultsResponse:
    results, total_results = await load_test_results_repository.filter_with_pagination(**query.model_dump())
    compares = await get_load_test_results_compares(
        query,
        results=results,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository
    )

    if len(results) == query.limit + 1:
        results = results[:-1]

    return GetLoadTestResultsResponse(
        items=[
            get_load_test_result_with_compare(result, compares[index])
            for index, result in enumerate(results)
        ],
        total=total_results,
        limit=query.limit,
        offset=query.offset
    )
