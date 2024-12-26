from typing import Annotated, TypedDict, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import IntegrationsModel
from services.postgres.models.integrations import IntegrationStatus
from utils.clients.postgres.repository import BasePostgresRepository


class UpdateIntegrationsModelDict(TypedDict, total=False):
    name: str
    cluster: str
    namespace: str
    environment_type: str


class CreateIntegrationsModelDict(UpdateIntegrationsModelDict):
    service_id: int


class IntegrationsRepository(BasePostgresRepository):
    model = IntegrationsModel

    async def get_by_id(self, integration_id: int) -> IntegrationsModel:
        return await self.model.get(
            self.session,
            clause_filter=(
                self.model.id == integration_id,
                self.model.status == IntegrationStatus.ACTIVE
            )
        )

    async def filter(self, service_id: int) -> Sequence[IntegrationsModel]:
        return await self.model.filter(
            self.session,
            order_by=(self.model.environment_type,),
            clause_filter=(
                self.model.status == IntegrationStatus.ACTIVE,
                self.model.service_id == service_id
            )
        )

    async def create(self, data: CreateIntegrationsModelDict) -> IntegrationsModel:
        return await self.model.create(self.session, **data)

    async def update(self, integration_id: int, data: UpdateIntegrationsModelDict) -> IntegrationsModel:
        return await self.model.update(
            self.session,
            clause_filter=(
                self.model.id == integration_id,
                self.model.status == IntegrationStatus.ACTIVE
            ),
            **data
        )

    async def delete(
            self,
            service_id: int | None = None,
            integration_id: int | None = None,
    ):
        filters = ()
        if service_id:
            filters += (self.model.service_id == service_id,)

        if integration_id:
            filters += (self.model.id == integration_id,)

        if not filters:
            return

        await self.model.update(
            self.session, clause_filter=filters, status=IntegrationStatus.DELETED
        )


async def get_integrations_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> IntegrationsRepository:
    return IntegrationsRepository(session=session)
