from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import IntegrationsModel
from services.postgres.models.base.status import ModelStatus
from utils.clients.postgres.repository import BasePostgresRepository


class IntegrationsRepository(BasePostgresRepository):
    model = IntegrationsModel

    async def get_by_id(self, integration_id: int) -> IntegrationsModel:
        return await self.model.get(
            self.session,
            clause_filter=(
                self.model.id == integration_id,
                self.model.status == ModelStatus.ACTIVE
            )
        )

    async def filter(self, service_id: int) -> Sequence[IntegrationsModel]:
        return await self.model.filter(
            self.session,
            order_by=(self.model.order_index,),
            clause_filter=(
                self.model.status == ModelStatus.ACTIVE,
                self.model.service_id == service_id
            )
        )

    async def create(self, data: dict) -> IntegrationsModel:
        return await self.model.create(self.session, **data)

    async def update(self, integration_id: int, data: dict) -> IntegrationsModel:
        return await self.model.update(
            self.session,
            clause_filter=(
                self.model.id == integration_id,
                self.model.status == ModelStatus.ACTIVE
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
            self.session, clause_filter=filters, status=ModelStatus.DELETED
        )


async def get_integrations_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> IntegrationsRepository:
    return IntegrationsRepository(session=session)
