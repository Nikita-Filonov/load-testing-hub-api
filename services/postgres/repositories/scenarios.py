from typing import Sequence, TypedDict, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import ScenariosModel
from services.postgres.models.ratio_results import RatioResultDict
from services.postgres.models.scenarios import ScenarioStatus
from utils.clients.postgres.repository import BasePostgresRepository


class UpdateScenariosModelDict(TypedDict, total=False):
    name: str
    file: str
    tags: list[str]
    version: str
    ratio_total: list[RatioResultDict]
    ratio_per_class: list[RatioResultDict]


class CreateScenariosModelDict(UpdateScenariosModelDict):
    service_id: str


class ScenariosRepository(BasePostgresRepository):
    model = ScenariosModel

    async def get_by_id(self, scenario_id: int) -> ScenariosModel | None:
        return await self.model.get(
            self.session,
            clause_filter=(
                self.model.id == scenario_id,
                self.model.status == ScenarioStatus.ACTIVE
            )
        )

    async def filter(self, service_id: int | None = None) -> Sequence[ScenariosModel]:
        filters = (self.model.status == ScenarioStatus.ACTIVE,)
        if service_id:
            filters += (self.model.service_id == service_id,)

        return await self.model.filter(
            self.session,
            order_by=(self.model.id,),
            clause_filter=filters
        )

    async def create(self, data: CreateScenariosModelDict) -> ScenariosModel:
        return await self.model.create(self.session, **data)

    async def update(self, scenario_id: int, data: CreateScenariosModelDict):
        return await self.model.update(
            self.session,
            clause_filter=(
                self.model.id == scenario_id,
                self.model.status == ScenarioStatus.ACTIVE
            ),
            **data
        )

    async def delete(
            self,
            service_id: int | None = None,
            scenario_id: int | None = None
    ):
        filters = ()
        if service_id:
            filters += (self.model.service_id == service_id,)

        if scenario_id:
            filters += (self.model.id == scenario_id,)

        if not filters:
            return

        await self.model.update(
            self.session, clause_filter=filters, status=ScenarioStatus.DELETED
        )


async def get_scenarios_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> ScenariosRepository:
    return ScenariosRepository(session=session)
