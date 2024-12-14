from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import MethodResultCompare, LoadTestResultCompare, \
    ResponseTimeCompareMetric, NumberOfUsersCompareMetric, MinResponseTimeCompareMetric, MaxResponseTimeCompareMetric, \
    NumberOfRequestsCompareMetric, NumberOfFailuresCompareMetric, RequestsPerSecondCompareMetric, \
    FailuresPerSecondCompareMetric, ContentLengthCompareMetric
from apps.compares.schema.compares.compare_result_with_averages import GetCompareResultWithAveragesQuery, \
    GetCompareResultWithAveragesResponse, CompareResultWithAverages
from services.postgres.models import MethodResultsModel, CompareSettingsModel
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.method_results import MethodResultsRepository, MethodResultsAverages


def get_method_result_compare(
        settings: CompareSettingsModel,
        method_result: MethodResultsModel,
        method_results_averages: MethodResultsAverages
) -> MethodResultCompare:
    return MethodResultCompare(
        method=method_result.method,
        settings=CompareSettings.model_validate(settings),
        response_time=ResponseTimeCompareMetric(
            actual=method_result.average_response_time,
            expected=method_results_averages.response_time
        ),
        content_length=ContentLengthCompareMetric(
            actual=method_result.average_content_length,
            expected=method_results_averages.content_length
        ),
        min_response_time=MinResponseTimeCompareMetric(
            actual=method_result.min_response_time,
            expected=method_results_averages.min_response_time
        ),
        max_response_time=MaxResponseTimeCompareMetric(
            actual=method_result.max_response_time,
            expected=method_results_averages.max_response_time
        ),
        number_of_requests=NumberOfRequestsCompareMetric(
            actual=method_result.number_of_requests,
            expected=method_results_averages.number_of_requests
        ),
        number_of_failures=NumberOfFailuresCompareMetric(
            actual=method_result.number_of_failures,
            expected=method_results_averages.number_of_failures
        ),
        requests_per_second=RequestsPerSecondCompareMetric(
            actual=method_result.requests_per_second,
            expected=method_results_averages.requests_per_second
        ),
        failures_per_second=FailuresPerSecondCompareMetric(
            actual=method_result.failures_per_second,
            expected=method_results_averages.failures_per_second
        ),
    )


async def get_compare_result_with_averages(
        query: GetCompareResultWithAveragesQuery,
        method_results_repository: MethodResultsRepository,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> GetCompareResultWithAveragesResponse:
    load_test_result = await load_test_results_repository.get_by_id(query.load_test_result_id)
    load_test_result_averages = await load_test_results_repository.get_averages(
        service_id=load_test_result.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    method_results = await method_results_repository.filter_by_load_test_result_id(query.load_test_result_id)
    method_results_averages = await method_results_repository.get_averages_for_methods(
        methods=[method_result.method for method_result in method_results],
        service_id=load_test_result.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    compare_settings = await compare_settings_repository.get_or_create(load_test_result.service_id)

    return GetCompareResultWithAveragesResponse(
        compare=CompareResultWithAverages(
            method_result_compares=[
                get_method_result_compare(
                    settings=compare_settings,
                    method_result=method_result,
                    method_results_averages=method_results_averages[method_result.method]
                )
                for method_result in method_results
            ],
            load_test_result_compare=LoadTestResultCompare(
                settings=CompareSettings.model_validate(compare_settings),
                response_time=ResponseTimeCompareMetric(
                    actual=load_test_result.average_response_time,
                    expected=load_test_result_averages.response_time
                ),
                number_of_users=NumberOfUsersCompareMetric(
                    actual=load_test_result.number_of_users,
                    expected=load_test_result_averages.number_of_users
                ),
                min_response_time=MinResponseTimeCompareMetric(
                    actual=load_test_result.min_response_time,
                    expected=load_test_result_averages.min_response_time
                ),
                max_response_time=MaxResponseTimeCompareMetric(
                    actual=load_test_result.max_response_time,
                    expected=load_test_result_averages.max_response_time
                ),
                number_of_requests=NumberOfRequestsCompareMetric(
                    actual=load_test_result.total_requests,
                    expected=load_test_result_averages.total_requests
                ),
                number_of_failures=NumberOfFailuresCompareMetric(
                    actual=load_test_result.total_failures,
                    expected=load_test_result.total_failures
                ),
                requests_per_second=RequestsPerSecondCompareMetric(
                    actual=load_test_result.total_requests_per_second,
                    expected=load_test_result_averages.total_requests_per_second
                ),
                failures_per_second=FailuresPerSecondCompareMetric(
                    actual=load_test_result.total_failures_per_second,
                    expected=load_test_result_averages.total_failures_per_second
                ),
            )
        )
    )
