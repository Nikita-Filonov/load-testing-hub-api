from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.ratio_results import GetRatioResultResponse, RootRatioResult, CreateRatioResultRequest
from services.postgres.models.ratio_results import RatioResultsModel


async def get_ratio_result(
        load_test_result_id: int,
        session: AsyncSession
) -> GetRatioResultResponse:
    results = await RatioResultsModel.get(
        session,
        clause_filter=(RatioResultsModel.load_test_results_id == load_test_result_id,)
    )
    if results is None:
        return GetRatioResultResponse()

    return GetRatioResultResponse(
        ratio_total=RootRatioResult.model_validate(results.ratio_total),
        ratio_per_class=RootRatioResult.model_validate(results.ratio_per_class),
    )


async def create_ratio_result(request: CreateRatioResultRequest, session: AsyncSession):
    await RatioResultsModel.create(session, **request.model_dump(mode='json'))
