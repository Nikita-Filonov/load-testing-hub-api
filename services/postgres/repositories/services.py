from typing import Sequence, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import undefer

from services.postgres.client import get_postgres_session
from services.postgres.models import ServicesModel
from services.postgres.models.base.status import ModelStatus
from utils.clients.postgres.repository import BasePostgresRepository


class ServicesRepository(BasePostgresRepository):
    model = ServicesModel

    async def get_by_id(self, service_id: int) -> ServicesModel | None:
        return await self.model.get(
            self.session,
            options=(
                undefer(self.model.number_of_scenarios),
                undefer(self.model.number_of_load_test_results)
            ),
            clause_filter=(
                self.model.id == service_id,
                self.model.status == ModelStatus.ACTIVE
            )
        )

    async def filter(self) -> Sequence[ServicesModel]:
        return await self.model.filter(
            self.session,
            options=(
                undefer(self.model.number_of_scenarios),
                undefer(self.model.number_of_load_test_results)
            ),
            order_by=(self.model.id,),
            clause_filter=(self.model.status == ModelStatus.ACTIVE,)
        )

    async def create(self, data: dict) -> ServicesModel:
        service = await self.model.create(self.session, **data)
        return await self.get_by_id(service.id)

    async def update(self, service_id: int, data: dict) -> ServicesModel | None:
        service = await self.model.update(
            self.session,
            clause_filter=(
                self.model.id == service_id,
                self.model.status == ModelStatus.ACTIVE
            ),
            **data
        )
        return await self.get_by_id(service.id)

    async def delete(self, service_id: int):
        await self.model.update(
            self.session,
            clause_filter=(self.model.id == service_id,),
            status=ModelStatus.DELETED
        )


async def get_services_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> ServicesRepository:
    return ServicesRepository(session=session)
