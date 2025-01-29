from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from services.postgres.client import get_postgres_session
from services.postgres.models import LoadTestResultsModel
from services.postgres.models.base.metrics import MetricsModelAverages
from services.postgres.models.base.number_of_users import NumberOfUsersModelAverages
from services.postgres.models.base.status import ModelStatus
from utils.clients.postgres.repository import BasePostgresRepository


@dataclass
class LoadTestResultsAverages(MetricsModelAverages, NumberOfUsersModelAverages):
    ...


class LoadTestResultsRepository(BasePostgresRepository):
    model = LoadTestResultsModel

    async def create(self, data: dict) -> LoadTestResultsModel:
        return await self.model.create(self.session, **data)

    async def delete(
            self,
            service_id: int | None = None,
            scenario_id: int | None = None,
            load_test_result_id: int | None = None
    ):
        filters = ()
        if service_id:
            filters += (self.model.service_id == service_id,)

        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        if load_test_result_id:
            filters += (self.model.id == load_test_result_id,)

        if not filters:
            return

        await self.model.update(
            self.session, clause_filter=filters, status=ModelStatus.DELETED
        )

    async def update(self, load_test_result_id: int, data: dict) -> LoadTestResultsModel:
        return await self.model.update(
            self.session,
            clause_filter=(
                self.model.id == load_test_result_id,
                self.model.status == ModelStatus.ACTIVE
            ),
            **data
        )

    async def filter(
            self,
            service_id: int | None = None,
            scenario_id: int | None = None,
            end_datetime: datetime | None = None,
            start_datetime: datetime | None = None
    ):
        filters = (self.model.status == ModelStatus.ACTIVE,)
        if service_id:
            filters += (self.model.service_id == service_id,)

        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        if end_datetime and start_datetime:
            filters += (self.model.created_at.between(start_datetime, end_datetime),)

        return await self.model.filter(
            self.session,
            order_by=(self.model.created_at,),
            clause_filter=filters
        )

    async def filter_with_pagination(
            self,
            limit: int,
            offset: int,
            service_id: int,
            started_at: datetime | None,
            finished_at: datetime | None,
            scenario_id: int | None,
            trigger_ci_project_version: str | None
    ) -> (Sequence[LoadTestResultsModel], int):
        filters = (
            self.model.status == ModelStatus.ACTIVE,
            self.model.service_id == service_id,
        )
        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        if started_at:
            filters += (self.model.started_at > started_at,)

        if finished_at:
            filters += (self.model.finished_at < finished_at,)

        if trigger_ci_project_version:
            filters += (
                func.lower(self.model.trigger_ci_project_version).contains(
                    trigger_ci_project_version.lower()
                ),
            )

        results = await self.model.filter(
            self.session,
            limit=limit,
            offset=offset,
            options=(joinedload(self.model.service), joinedload(self.model.scenario)),
            order_by=(self.model.created_at.desc(),),
            clause_filter=filters
        )
        total_results = await self.model.count(self.session, column=self.model.id, clause_filter=filters)

        return results, total_results

    async def get_by_id(self, load_test_result_id: int) -> LoadTestResultsModel | None:
        return await self.model.get(
            self.session,
            options=(joinedload(self.model.service), joinedload(self.model.scenario)),
            clause_filter=(
                self.model.id == load_test_result_id,
                self.model.status == ModelStatus.ACTIVE
            )
        )

    async def get_previous(
            self,
            service_id: int,
            scenario_id: int | None,
            load_test_result_id: int
    ) -> LoadTestResultsModel | None:
        filters = (
            self.model.id < load_test_result_id,
            self.model.status == ModelStatus.ACTIVE,
            self.model.service_id == service_id
        )
        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        previous_results = await self.model.filter(
            self.session, limit=1, order_by=(self.model.id.desc(),), clause_filter=filters
        )

        return previous_results[0] if len(previous_results) > 0 else None

    async def filter_by_ids(self, ids: list[int]) -> Sequence[LoadTestResultsModel]:
        return await self.model.filter(
            self.session,
            options=(joinedload(self.model.service), joinedload(self.model.scenario)),
            clause_filter=(
                self.model.id.in_(ids),
                self.model.status == ModelStatus.ACTIVE
            )
        )

    async def filter_by_ids_groped(self, ids: list[int]) -> dict[int, LoadTestResultsModel]:
        results = await self.model.filter(
            self.session,
            order_by=(self.model.id.asc(),),
            clause_filter=(
                self.model.id.in_(ids),
                self.model.status == ModelStatus.ACTIVE
            )
        )

        return {result.id: result for result in results}

    async def get_averages(
            self,
            service_id: int,
            scenario_id: int | None = None,
            end_datetime: datetime | None = None,
            start_datetime: datetime | None = None
    ) -> LoadTestResultsAverages:
        filters = (
            self.model.service_id == service_id,
            self.model.status == ModelStatus.ACTIVE
        )
        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        if end_datetime and start_datetime:
            filters += (self.model.created_at.between(start_datetime, end_datetime),)

        averages = await self.model.averages(
            self.session,
            columns=self.model.get_average_allowed_columns(),
            clause_filter=filters
        )

        return LoadTestResultsAverages(**averages)


async def get_load_test_results_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> LoadTestResultsRepository:
    return LoadTestResultsRepository(session=session)
