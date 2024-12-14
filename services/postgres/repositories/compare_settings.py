from typing import Annotated, TypedDict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import CompareSettingsModel
from utils.clients.postgres.repository import BasePostgresRepository


class UpdateCompareSettingsModelDict(TypedDict):
    response_time_weight: float
    min_response_time_weight: float
    max_response_time_weight: float
    number_of_requests_weight: float
    number_of_failures_weight: float
    requests_per_second_weight: float
    failures_per_second_weight: float


class CompareSettingsRepository(BasePostgresRepository):
    model = CompareSettingsModel

    async def get_or_create(self, service_id: int) -> CompareSettingsModel:
        settings = await self.model.get(self.session, service_id=service_id)

        if not settings:
            settings = await self.model.create(self.session, service_id=service_id)

        return settings

    async def update(self, service_id: int, data: UpdateCompareSettingsModelDict) -> CompareSettingsModel:
        return await self.model.update(
            self.session, clause_filter=(self.model.service_id == service_id,), **data
        )


async def get_compare_settings_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> CompareSettingsRepository:
    return CompareSettingsRepository(session=session)
