from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import RatioResultsModel
from utils.clients.postgres.repository import BasePostgresRepository


class RatioResultsRepository(BasePostgresRepository):
    model = RatioResultsModel

    async def get_by_load_test_result_id(
            self,
            load_test_result_id: int
    ) -> RatioResultsModel | None:
        return await self.model.get(
            self.session, clause_filter=(self.model.load_test_result_id == load_test_result_id,)
        )

    async def create(self, data: dict) -> RatioResultsModel:
        return await self.model.create(self.session, **data)


async def get_ratio_results_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> RatioResultsRepository:
    return RatioResultsRepository(session=session)
