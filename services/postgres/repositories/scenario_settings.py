from typing import Annotated, TypedDict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import ScenarioSettingsModel
from services.postgres.models.scenario_settings import ScenarioMethodSettingsDict
from utils.clients.postgres.repository import BasePostgresRepository


class UpdateScenarioSettingsModelDict(TypedDict, total=False):
    response_time: float
    number_of_users: float
    min_response_time: float
    max_response_time: float
    number_of_requests: float
    number_of_failures: float
    requests_per_second: float
    failures_per_second: float

    methods_settings: list[ScenarioMethodSettingsDict]


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

    async def update(
            self,
            scenario_id: int,
            data: UpdateScenarioSettingsModelDict
    ) -> ScenarioSettingsModel:
        return await self.model.update(
            self.session, clause_filter=(self.model.scenario_id == scenario_id,), **data
        )


async def get_scenario_settings_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> ScenarioSettingsRepository:
    return ScenarioSettingsRepository(session=session)
