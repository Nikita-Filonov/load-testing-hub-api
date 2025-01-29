from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import ScenarioSettingsModel
from utils.clients.postgres.repository import BasePostgresRepository


class ScenarioSettingsRepository(BasePostgresRepository):
    model = ScenarioSettingsModel

    async def get_by_scenario_id(self, scenario_id: int) -> ScenarioSettingsModel | None:
        return await self.model.get(
            self.session, clause_filter=(self.model.scenario_id == scenario_id,)
        )

    async def get_or_create(self, scenario_id: int) -> ScenarioSettingsModel:
        settings = await self.get_by_scenario_id(scenario_id)

        if not settings:
            settings = await self.model.create(self.session, scenario_id=scenario_id)

        return settings

    async def update(self, scenario_id: int, data: dict) -> ScenarioSettingsModel:
        return await self.model.update(
            self.session, clause_filter=(self.model.scenario_id == scenario_id,), **data
        )


async def get_scenario_settings_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> ScenarioSettingsRepository:
    return ScenarioSettingsRepository(session=session)
