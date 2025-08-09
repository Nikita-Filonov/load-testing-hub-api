from typing import Sequence

from apps.compares.constants.compare_settings.context import CompareSettingsContext
from apps.compares.controllers.compares.compare_result_with_results.summary import (
    get_compare_result_with_results_average_summary
)
from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import (
    MethodResultCompare,
    LoadTestResultCompare,
    BuildBaseCompareParams,
    BuildMethodResultCompare
)
from apps.compares.schema.compares.compare_result_with_results import (
    CompareResultWithResults,
    GetCompareResultWithResultsQuery,
    GetCompareResultWithResultsResponse,
)
from apps.results.schema.load_test_results.results import ShortLoadTestResult
from services.postgres.models import LoadTestResultsModel, MethodResultsModel, CompareSettingsModel
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.method_results import MethodResultsRepository


def get_method_result_compare(
        settings: CompareSettingsModel,
        method_result: MethodResultsModel,
        compare_with_method_result: MethodResultsModel,
) -> MethodResultCompare:
    return MethodResultCompare.build(
        BuildMethodResultCompare(
            method=method_result.method,
            context=CompareSettingsContext.COMPARE_RESULT_WITH_RESULTS,
            settings=CompareSettings.model_validate(settings),
            actual_instance=method_result,
            expected_instance=compare_with_method_result
        )
    )


def get_single_compare_result_with_results(
        settings: CompareSettingsModel,
        method_results: Sequence[MethodResultsModel],
        load_test_result: LoadTestResultsModel,
        compare_with_method_results: Sequence[MethodResultsModel],
        compare_with_load_test_result: LoadTestResultsModel
) -> CompareResultWithResults:
    compare_with_method_results = sorted(compare_with_method_results, key=lambda r: r.method)

    return CompareResultWithResults(
        method_result_compares=[
            get_method_result_compare(settings, method_result, compare_with_method_result)
            for method_result, compare_with_method_result
            in zip(method_results, compare_with_method_results)
        ],
        load_test_result_compare=LoadTestResultCompare.build(
            BuildBaseCompareParams(
                context=CompareSettingsContext.COMPARE_RESULT_WITH_RESULTS,
                settings=CompareSettings.model_validate(settings),
                actual_instance=load_test_result,
                expected_instance=compare_with_load_test_result,
            )
        ),
        compare_with_load_test_result=ShortLoadTestResult.model_validate(compare_with_load_test_result),
    )


async def get_compare_result_with_results(
        query: GetCompareResultWithResultsQuery,
        method_results_repository: MethodResultsRepository,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> GetCompareResultWithResultsResponse:
    load_test_result = await load_test_results_repository.get_by_id(query.load_test_result_id)
    compare_with_load_test_results = await load_test_results_repository.filter_by_ids(
        query.compare_with_load_test_results
    )

    method_results = await method_results_repository.filter_by_load_test_result_id(query.load_test_result_id)
    compare_with_method_results = await method_results_repository.filter_by_load_test_result_ids_groped(
        query.compare_with_load_test_results
    )

    compare_settings = await compare_settings_repository.get_or_create(load_test_result.service_id)

    compares = [
        get_single_compare_result_with_results(
            settings=compare_settings,
            method_results=method_results,
            load_test_result=load_test_result,
            compare_with_method_results=compare_with_method_results.get(compare_with_load_test_result.id, []),
            compare_with_load_test_result=compare_with_load_test_result
        )
        for compare_with_load_test_result in compare_with_load_test_results
    ]

    return GetCompareResultWithResultsResponse(
        summary=get_compare_result_with_results_average_summary(
            compares=compares,
            settings=compare_settings,
            method_results=method_results,
            load_test_result=load_test_result
        ),
        compares=compares
    )
