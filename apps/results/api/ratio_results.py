from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.ratio_results import get_ratio_result, create_ratio_result
from apps.results.schema.ratio_results import GetRatioResultResponse, CreateRatioResultRequest
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

ratio_results_router = APIRouter(
    prefix=APIRoutes.RATIO_RESULTS,
    tags=[APIRoutes.RATIO_RESULTS.as_tag()]
)


@ratio_results_router.get('/{load_test_result_id}', response_model=GetRatioResultResponse)
async def get_ratio_result_view(
        load_test_result_id: int,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_ratio_result(load_test_result_id, session)


@ratio_results_router.post('')
async def create_ratio_result_view(
        request: CreateRatioResultRequest,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await create_ratio_result(request, session)
