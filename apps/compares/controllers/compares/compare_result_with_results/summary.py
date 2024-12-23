from itertools import chain
from typing import Sequence

from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import MethodResultCompare, LoadTestResultCompare, \
    ResponseTimeCompareMetric, ContentLengthCompareMetric, MinResponseTimeCompareMetric, MaxResponseTimeCompareMetric, \
    NumberOfRequestsCompareMetric, NumberOfFailuresCompareMetric, RequestsPerSecondCompareMetric, \
    FailuresPerSecondCompareMetric, NumberOfUsersCompareMetric
from apps.compares.schema.compares.compare_result_with_results import CompareResultWithResults, \
    CompareResultWithResultsAverageSummary
from services.postgres.models import LoadTestResultsModel, MethodResultsModel, CompareSettingsModel
from services.postgres.models.compare_settings import CompareSettingsContext
from utils.common.average import get_average


def get_method_result_compare_average_summary(
        compares: list[CompareResultWithResults],
        settings: CompareSettingsModel,
        method_result: MethodResultsModel,
) -> MethodResultCompare:
    method_compares = [
        compare for compare in chain.from_iterable([compare.method_result_compares for compare in compares])
        if compare.method == method_result.method
    ]

    (
        response_time,
        content_length,
        min_response_time,
        max_response_time,
        number_of_requests,
        number_of_failures,
        requests_per_second,
        failures_per_second
    ) = (
        [compare.response_time.expected for compare in method_compares],
        [compare.content_length.expected for compare in method_compares],
        [compare.min_response_time.expected for compare in method_compares],
        [compare.max_response_time.expected for compare in method_compares],
        [compare.number_of_requests.expected for compare in method_compares],
        [compare.number_of_failures.expected for compare in method_compares],
        [compare.requests_per_second.expected for compare in method_compares],
        [compare.failures_per_second.expected for compare in method_compares],
    )

    return MethodResultCompare(
        method=method_result.method,
        context=CompareSettingsContext.COMPARE_RESULT_WITH_RESULTS,
        settings=CompareSettings.model_validate(settings),
        response_time=ResponseTimeCompareMetric(
            actual=method_result.average_response_time,
            expected=get_average(response_time)
        ),
        content_length=ContentLengthCompareMetric(
            actual=method_result.average_content_length,
            expected=get_average(content_length)
        ),
        min_response_time=MinResponseTimeCompareMetric(
            actual=method_result.min_response_time,
            expected=get_average(min_response_time)
        ),
        max_response_time=MaxResponseTimeCompareMetric(
            actual=method_result.max_response_time,
            expected=get_average(max_response_time)
        ),
        number_of_requests=NumberOfRequestsCompareMetric(
            actual=method_result.number_of_requests,
            expected=get_average(number_of_requests)
        ),
        number_of_failures=NumberOfFailuresCompareMetric(
            actual=method_result.number_of_failures,
            expected=get_average(number_of_failures)
        ),
        requests_per_second=RequestsPerSecondCompareMetric(
            actual=method_result.requests_per_second,
            expected=get_average(requests_per_second)
        ),
        failures_per_second=FailuresPerSecondCompareMetric(
            actual=method_result.failures_per_second,
            expected=get_average(failures_per_second)
        ),
    )


def get_load_test_compare_averages_summary(
        compares: list[CompareResultWithResults],
        settings: CompareSettingsModel,
        load_test_result: LoadTestResultsModel,
) -> LoadTestResultCompare:
    (
        response_time,
        number_of_users,
        min_response_time,
        max_response_time,
        number_of_requests,
        number_of_failures,
        requests_per_second,
        failures_per_second
    ) = (
        [compare.load_test_result_compare.response_time.expected for compare in compares],
        [compare.load_test_result_compare.number_of_users.expected for compare in compares],
        [compare.load_test_result_compare.min_response_time.expected for compare in compares],
        [compare.load_test_result_compare.max_response_time.expected for compare in compares],
        [compare.load_test_result_compare.number_of_requests.expected for compare in compares],
        [compare.load_test_result_compare.number_of_failures.expected for compare in compares],
        [compare.load_test_result_compare.requests_per_second.expected for compare in compares],
        [compare.load_test_result_compare.failures_per_second.expected for compare in compares]
    )

    return LoadTestResultCompare(
        context=CompareSettingsContext.COMPARE_RESULT_WITH_RESULTS,
        settings=CompareSettings.model_validate(settings),
        response_time=ResponseTimeCompareMetric(
            actual=load_test_result.average_response_time,
            expected=get_average(response_time)
        ),
        number_of_users=NumberOfUsersCompareMetric(
            actual=load_test_result.number_of_users,
            expected=get_average(number_of_users)
        ),
        min_response_time=MinResponseTimeCompareMetric(
            actual=load_test_result.min_response_time,
            expected=get_average(min_response_time)
        ),
        max_response_time=MaxResponseTimeCompareMetric(
            actual=load_test_result.max_response_time,
            expected=get_average(max_response_time)
        ),
        number_of_requests=NumberOfRequestsCompareMetric(
            actual=load_test_result.total_requests,
            expected=get_average(number_of_requests)
        ),
        number_of_failures=NumberOfFailuresCompareMetric(
            actual=load_test_result.total_failures,
            expected=get_average(number_of_failures)
        ),
        requests_per_second=RequestsPerSecondCompareMetric(
            actual=load_test_result.total_requests_per_second,
            expected=get_average(requests_per_second)
        ),
        failures_per_second=FailuresPerSecondCompareMetric(
            actual=load_test_result.total_failures_per_second,
            expected=get_average(failures_per_second)
        ),
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
