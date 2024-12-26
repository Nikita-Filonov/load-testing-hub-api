from typing import Sequence, Annotated, TypedDict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import ServicesModel
from services.postgres.models.services import ServiceStatus
from utils.clients.postgres.repository import BasePostgresRepository


class CreateServiceModelDict(TypedDict):
    url: str
    name: str
    cluster: str
    namespace: str


class ServicesRepository(BasePostgresRepository):
    model = ServicesModel

    async def get_by_id(self, service_id: int) -> ServicesModel | None:
        return await self.model.get(
            self.session,
            clause_filter=(
                self.model.id == service_id,
                self.model.status == ServiceStatus.ACTIVE
            )
        )

    async def filter(self) -> Sequence[ServicesModel]:
        return await self.model.filter(
            self.session,
            order_by=(self.model.id,),
            clause_filter=(self.model.status == ServiceStatus.ACTIVE,)
        )

    async def create(self, data: CreateServiceModelDict) -> ServicesModel:
        return await self.model.create(self.session, **data)

    async def update(self, service_id: int, data: CreateServiceModelDict):
        return await self.model.update(
            self.session,
            clause_filter=(
                self.model.id == service_id,
                self.model.status == ServiceStatus.ACTIVE
            ),
            **data
        )

    async def delete(self, service_id: int):
        await self.model.update(
            self.session,
            clause_filter=(self.model.id == service_id,),
            status=ServiceStatus.DELETED
        )


async def get_services_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> ServicesRepository:
    return ServicesRepository(session=session)
