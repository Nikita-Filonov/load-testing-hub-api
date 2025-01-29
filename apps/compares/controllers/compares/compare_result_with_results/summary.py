from itertools import chain
from typing import Sequence

from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import MethodResultCompare, LoadTestResultCompare, \
    BuildMethodResultCompare, BuildBaseCompareParams
from apps.compares.schema.compares.compare_result_with_results import CompareResultWithResults, \
    CompareResultWithResultsAverageSummary, MethodResultCompareAverageSummary, LoadTestCompareAveragesSummary
from services.postgres.models import LoadTestResultsModel, MethodResultsModel, CompareSettingsModel
from services.postgres.models.compare_settings import CompareSettingsContext
from utils.base.average import get_average


def get_method_result_compare_average_summary(
        compares: list[CompareResultWithResults],
        settings: CompareSettingsModel,
        method_result: MethodResultsModel,
) -> MethodResultCompare:
    method_compares: list[MethodResultCompare] = chain.from_iterable(
        [compare.method_result_compares for compare in compares]
    )
    method_compares: list[MethodResultCompare] = [
        compare for compare in method_compares
        if compare.method == method_result.method
    ]

    average_summary = MethodResultCompareAverageSummary(**{
        metric_key.value: get_average([
            getattr(compare, metric_key.value).expected
            for compare in method_compares
        ])
        for metric_key in MethodResultCompare.get_metric_keys()
    })

    return MethodResultCompare.build(
        BuildMethodResultCompare(
            method=method_result.method,
            context=CompareSettingsContext.COMPARE_RESULT_WITH_RESULTS,
            settings=CompareSettings.model_validate(settings),
            actual_instance=method_result,
            expected_instance=average_summary
        )
    )


def get_load_test_compare_averages_summary(
        compares: list[CompareResultWithResults],
        settings: CompareSettingsModel,
        load_test_result: LoadTestResultsModel,
) -> LoadTestResultCompare:
    average_summary = LoadTestCompareAveragesSummary(**{
        metric_key.value: get_average([
            getattr(compare.load_test_result_compare, metric_key.value).expected
            for compare in compares
        ])
        for metric_key in LoadTestResultCompare.get_metric_keys()
    })

    return LoadTestResultCompare.build(
        BuildBaseCompareParams(
            context=CompareSettingsContext.COMPARE_RESULT_WITH_RESULTS,
            settings=CompareSettings.model_validate(settings),
            actual_instance=load_test_result,
            expected_instance=average_summary
        )
    )


def get_compare_result_with_results_average_summary(
        compares: list[CompareResultWithResults],
        settings: CompareSettingsModel,
        method_results: Sequence[MethodResultsModel],
        load_test_result: LoadTestResultsModel,
) -> CompareResultWithResultsAverageSummary:
    return CompareResultWithResultsAverageSummary(
        method_result_compares=[
            get_method_result_compare_average_summary(
                compares=compares,
                settings=settings,
                method_result=method_result
            )
            for method_result in method_results
        ],
        load_test_result_compare=get_load_test_compare_averages_summary(
            compares=compares, settings=settings, load_test_result=load_test_result
        ),
    )
