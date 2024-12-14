from apps.compares.schema.compare_settings import CompareSettings, \
    UpdateCompareSettingsRequest, GetCompareSettingsResponse
from services.postgres.repositories.compare_settings import CompareSettingsRepository


async def get_or_create_compare_settings(
        service_id: int,
        compare_settings_repository: CompareSettingsRepository
) -> GetCompareSettingsResponse:
    settings = await compare_settings_repository.get_or_create(service_id)

    return GetCompareSettingsResponse(settings=CompareSettings.model_validate(settings))


async def update_compare_settings(
        service_id: int,
        request: UpdateCompareSettingsRequest,
        compare_settings_repository: CompareSettingsRepository
) -> GetCompareSettingsResponse:
    settings = await compare_settings_repository.update(
        service_id, request.model_dump(exclude_unset=True)
    )

    return GetCompareSettingsResponse(settings=CompareSettings.model_validate(settings))
