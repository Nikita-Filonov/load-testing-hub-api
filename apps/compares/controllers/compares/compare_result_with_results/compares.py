from typing import Sequence

from apps.compares.controllers.compares.compare_result_with_results.summary import \
    get_compare_result_with_results_average_summary
from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import MethodResultCompare, LoadTestResultCompare, \
    ResponseTimeCompareMetric, ContentLengthCompareMetric, MinResponseTimeCompareMetric, MaxResponseTimeCompareMetric, \
    NumberOfRequestsCompareMetric, NumberOfFailuresCompareMetric, RequestsPerSecondCompareMetric, \
    FailuresPerSecondCompareMetric, NumberOfUsersCompareMetric
from apps.compares.schema.compares.compare_result_with_results import GetCompareResultWithResultsQuery, \
    GetCompareResultWithResultsResponse, CompareResultWithResults
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
    return MethodResultCompare(
        method=method_result.method,
        settings=CompareSettings.model_validate(settings),
        response_time=ResponseTimeCompareMetric(
            actual=method_result.average_response_time,
            expected=compare_with_method_result.average_response_time
        ),
        content_length=ContentLengthCompareMetric(
            actual=method_result.average_content_length,
            expected=compare_with_method_result.average_content_length
        ),
        min_response_time=MinResponseTimeCompareMetric(
            actual=method_result.min_response_time,
            expected=compare_with_method_result.min_response_time
        ),
        max_response_time=MaxResponseTimeCompareMetric(
            actual=method_result.max_response_time,
            expected=compare_with_method_result.max_response_time
        ),
        number_of_requests=NumberOfRequestsCompareMetric(
            actual=method_result.number_of_requests,
            expected=compare_with_method_result.number_of_requests
        ),
        number_of_failures=NumberOfFailuresCompareMetric(
            actual=method_result.number_of_failures,
            expected=compare_with_method_result.number_of_failures
        ),
        requests_per_second=RequestsPerSecondCompareMetric(
            actual=method_result.requests_per_second,
            expected=compare_with_method_result.requests_per_second
        ),
        failures_per_second=FailuresPerSecondCompareMetric(
            actual=method_result.failures_per_second,
            expected=compare_with_method_result.failures_per_second
        ),
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
        load_test_result_compare=LoadTestResultCompare(
            settings=CompareSettings.model_validate(settings),
            response_time=ResponseTimeCompareMetric(
                actual=load_test_result.average_response_time,
                expected=compare_with_load_test_result.average_response_time
            ),
            number_of_users=NumberOfUsersCompareMetric(
                actual=load_test_result.number_of_users,
                expected=compare_with_load_test_result.number_of_users
            ),
            min_response_time=MinResponseTimeCompareMetric(
                actual=load_test_result.min_response_time,
                expected=compare_with_load_test_result.min_response_time
            ),
            max_response_time=MaxResponseTimeCompareMetric(
                actual=load_test_result.max_response_time,
                expected=compare_with_load_test_result.max_response_time
            ),
            number_of_requests=NumberOfRequestsCompareMetric(
                actual=load_test_result.total_requests,
                expected=compare_with_load_test_result.total_requests
            ),
            number_of_failures=NumberOfFailuresCompareMetric(
                actual=load_test_result.total_failures,
                expected=compare_with_load_test_result.total_failures
            ),
            requests_per_second=RequestsPerSecondCompareMetric(
                actual=load_test_result.total_requests_per_second,
                expected=compare_with_load_test_result.total_requests_per_second
            ),
            failures_per_second=FailuresPerSecondCompareMetric(
                actual=load_test_result.total_failures_per_second,
                expected=compare_with_load_test_result.total_failures_per_second
            ),
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
