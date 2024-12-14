from typing import Annotated

from fastapi import APIRouter, Depends

from apps.compares.controllers.compare_settings import get_or_create_compare_settings, update_compare_settings
from apps.compares.schema.compare_settings import GetCompareSettingsResponse, UpdateCompareSettingsRequest
from services.postgres.repositories.compare_settings import CompareSettingsRepository, get_compare_settings_repository
from utils.routes import APIRoutes

compare_settings_router = APIRouter(
    prefix=APIRoutes.COMPARE_SETTINGS,
    tags=[APIRoutes.COMPARE_SETTINGS.as_tag()]
)


@compare_settings_router.get('/{service_id}', response_model=GetCompareSettingsResponse)
async def get_compare_settings_view(
        service_id: int,
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)]
):
    return await get_or_create_compare_settings(service_id, compare_settings_repository)


@compare_settings_router.patch('/{service_id}', response_model=GetCompareSettingsResponse)
async def update_compare_settings_view(
        service_id: int,
        request: UpdateCompareSettingsRequest,
        compare_settings_repository: Annotated[CompareSettingsRepository, Depends(get_compare_settings_repository)]
):
    return await update_compare_settings(service_id, request, compare_settings_repository)
