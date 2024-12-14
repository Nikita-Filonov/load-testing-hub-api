from apps.results.controllers.load_test_results.details import get_load_test_result_details
from apps.results.schema.load_test_results.results import GetLoadTestResultDetailsResponse, \
    CreateLoadTestResultRequest, UpdateLoadTestResultRequest, GetLoadTestResultDetailsQuery, UpdateLoadTestResultQuery
from services.postgres.repositories.compare_settings import CompareSettingsRepository
from services.postgres.repositories.load_test_results import LoadTestResultsRepository


async def create_load_test_result(
        request: CreateLoadTestResultRequest,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> GetLoadTestResultDetailsResponse:
    result = await load_test_results_repository.create(request.model_dump())

    return await get_load_test_result_details(
        result.id,
        query=GetLoadTestResultDetailsQuery(scenario_id=result.scenario_id),
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository
    )


async def delete_load_test_result(
        load_test_result_id: int,
        load_test_results_repository: LoadTestResultsRepository
):
    await load_test_results_repository.delete(load_test_result_id=load_test_result_id)


async def update_load_test_result(
        load_test_result_id: int,
        query: UpdateLoadTestResultQuery,
        request: UpdateLoadTestResultRequest,
        compare_settings_repository: CompareSettingsRepository,
        load_test_results_repository: LoadTestResultsRepository
) -> GetLoadTestResultDetailsResponse:
    await load_test_results_repository.update(load_test_result_id, request.model_dump(exclude_unset=True))

    return await get_load_test_result_details(
        load_test_result_id,
        query=query,
        compare_settings_repository=compare_settings_repository,
        load_test_results_repository=load_test_results_repository
    )
