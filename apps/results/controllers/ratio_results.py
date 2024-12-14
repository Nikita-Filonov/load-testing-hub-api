from apps.results.schema.ratio_results import GetRatioResultResponse, RootRatioResult, CreateRatioResultRequest
from services.postgres.repositories.ratio_results import RatioResultsRepository


async def get_ratio_result(
        load_test_result_id: int,
        ratio_results_repository: RatioResultsRepository
) -> GetRatioResultResponse:
    results = await ratio_results_repository.get_by_load_test_result_id(load_test_result_id)
    if results is None:
        return GetRatioResultResponse()

    return GetRatioResultResponse(
        ratio_total=RootRatioResult.model_validate(results.ratio_total),
        ratio_per_class=RootRatioResult.model_validate(results.ratio_per_class),
    )


async def create_ratio_result(
        request: CreateRatioResultRequest,
        ratio_results_repository: RatioResultsRepository
):
    await ratio_results_repository.create(request.model_dump(mode='json'))
