from apps.results.controllers.load_test_results.compares import get_load_test_result_summary_compare
from apps.results.schema.load_test_results.results import LoadTestResultDetails, GetLoadTestResultDetailsResponse, \
    GetLoadTestResultDetailsQuery
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository


async def get_load_test_result_details(
        load_test_result_id: int,
        query: GetLoadTestResultDetailsQuery,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> GetLoadTestResultDetailsResponse:
    result = await load_test_results_repository.get_by_id(load_test_result_id)
    previous_result = await load_test_results_repository.get_previous(
        service_id=result.service_id,
        scenario_id=query.scenario_id,
        load_test_result_id=load_test_result_id
    )

    compare_settings = await compare_settings_repository.get_or_create(result.service_id)
    load_test_result_averages = await load_test_results_repository.get_averages(
        service_id=result.service_id, scenario_id=query.scenario_id
    )

    details = LoadTestResultDetails.model_validate(result)
    details.compare = get_load_test_result_summary_compare(
        result=result,
        previous_result=previous_result,
        compare_settings=compare_settings,
        load_test_result_averages=load_test_result_averages
    )

    return GetLoadTestResultDetailsResponse(details=details)
