from typing import Annotated

from fastapi import APIRouter, Depends

from apps.results.controllers.ratio_results import get_ratio_result, create_ratio_result
from apps.results.schema.ratio_results import GetRatioResultResponse, CreateRatioResultRequest
from services.postgres.repositories.ratio_results import get_ratio_results_repository, RatioResultsRepository
from utils.routes import APIRoutes

ratio_results_router = APIRouter(
    prefix=APIRoutes.RATIO_RESULTS,
    tags=[APIRoutes.RATIO_RESULTS.as_tag()]
)


@ratio_results_router.get('/{load_test_result_id}', response_model=GetRatioResultResponse)
async def get_ratio_result_view(
        load_test_result_id: int,
        ratio_results_repository: Annotated[RatioResultsRepository, Depends(get_ratio_results_repository)]
):
    return await get_ratio_result(load_test_result_id, ratio_results_repository)


@ratio_results_router.post('')
async def create_ratio_result_view(
        request: CreateRatioResultRequest,
        ratio_results_repository: Annotated[RatioResultsRepository, Depends(get_ratio_results_repository)]
):
    return await create_ratio_result(request, ratio_results_repository)
