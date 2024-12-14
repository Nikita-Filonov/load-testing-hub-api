from apps.compares.schema.compare_settings import CompareSettings
from apps.compares.schema.compares.compare import LoadTestResultCompare, ResponseTimeCompareMetric, \
    MinResponseTimeCompareMetric, MaxResponseTimeCompareMetric, NumberOfUsersCompareMetric, \
    NumberOfRequestsCompareMetric, NumberOfFailuresCompareMetric, RequestsPerSecondCompareMetric, \
    FailuresPerSecondCompareMetric
from apps.compares.schema.compares.compare_averages_with_scenario import GetCompareAveragesWithScenarioQuery, \
    GetCompareAveragesWithScenarioResponse
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository
from services.postgres.repositories.scenario_settings import ScenarioSettingsRepository


async def get_compare_averages_with_scenario(
        query: GetCompareAveragesWithScenarioQuery,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository,
        scenario_settings_repository: ScenarioSettingsRepository,
) -> GetCompareAveragesWithScenarioResponse:
    load_test_result_averages = await load_test_results_repository.get_averages(
        service_id=query.service_id,
        scenario_id=query.scenario_id,
        end_datetime=query.end_datetime,
        start_datetime=query.start_datetime
    )

    compare_settings = await compare_settings_repository.get_or_create(query.service_id)
    scenario_settings = await scenario_settings_repository.get_or_create(query.scenario_id)

    return GetCompareAveragesWithScenarioResponse(
        compare=LoadTestResultCompare(
            settings=CompareSettings.model_validate(compare_settings),
            response_time=ResponseTimeCompareMetric(
                actual=load_test_result_averages.response_time,
                expected=scenario_settings.response_time
            ),
            number_of_users=NumberOfUsersCompareMetric(
                actual=load_test_result_averages.number_of_users,
                expected=scenario_settings.number_of_users
            ),
            min_response_time=MinResponseTimeCompareMetric(
                actual=load_test_result_averages.min_response_time,
                expected=scenario_settings.min_response_time
            ),
            max_response_time=MaxResponseTimeCompareMetric(
                actual=load_test_result_averages.max_response_time,
                expected=scenario_settings.max_response_time
            ),
            number_of_requests=NumberOfRequestsCompareMetric(
                actual=load_test_result_averages.total_requests,
                expected=scenario_settings.number_of_requests
            ),
            number_of_failures=NumberOfFailuresCompareMetric(
                actual=load_test_result_averages.total_failures,
                expected=scenario_settings.number_of_failures
            ),
            requests_per_second=RequestsPerSecondCompareMetric(
                actual=load_test_result_averages.total_requests_per_second,
                expected=scenario_settings.requests_per_second
            ),
            failures_per_second=FailuresPerSecondCompareMetric(
                actual=load_test_result_averages.total_failures_per_second,
                expected=scenario_settings.failures_per_second
            ),
        )
    )
