from datetime import datetime
from typing import Annotated, Sequence, NamedTuple, TypedDict

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from services.postgres.client import get_postgres_session
from services.postgres.models import LoadTestResultsModel
from services.postgres.models.load_test_results import LoadTestResultStatus
from utils.clients.postgres.repository import BasePostgresRepository


class LoadTestResultsAverages(NamedTuple):
    response_time: float | None
    total_requests: float | None
    total_failures: float | None
    number_of_users: float | None
    min_response_time: float | None
    max_response_time: float | None
    total_requests_per_second: float | None
    total_failures_per_second: float | None


class UpdateLoadTestResultsModelDict(TypedDict):
    comment: str | None


class CreateLoadTestResultsModelDict(UpdateLoadTestResultsModelDict):
    trigger_ci_job_url: str | None
    trigger_ci_pipeline_url: str | None
    trigger_ci_project_version: str | None
    load_tests_ci_job_url: str | None
    load_tests_ci_pipeline_url: str | None
    number_of_users: int
    total_requests: int
    total_failures: int
    max_response_time: float
    min_response_time: float
    average_response_time: float
    total_requests_per_second: float
    total_failures_per_second: float
    created_at: datetime
    started_at: datetime
    finished_at: datetime

    service_id: int
    scenario_id: int


class LoadTestResultsRepository(BasePostgresRepository):
    model = LoadTestResultsModel

    async def create(self, data: CreateLoadTestResultsModelDict) -> LoadTestResultsModel:
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
            self.session, clause_filter=filters, status=LoadTestResultStatus.DELETED
        )

    async def update(
            self,
            load_test_result_id: int,
            data: UpdateLoadTestResultsModelDict
    ) -> LoadTestResultsModel:
        return await self.model.update(
            self.session,
            clause_filter=(
                self.model.id == load_test_result_id,
                self.model.status == LoadTestResultStatus.ACTIVE
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
        filters = (self.model.status == LoadTestResultStatus.ACTIVE,)
        if service_id:
            filters += (self.model.service_id == service_id,)

        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        if end_datetime and start_datetime:
            filters += (self.model.created_at.between(start_datetime, end_datetime),)

        return await self.model.filter(self.session, clause_filter=filters)

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
            self.model.status == LoadTestResultStatus.ACTIVE,
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
                self.model.status == LoadTestResultStatus.ACTIVE
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
            self.model.status == LoadTestResultStatus.ACTIVE,
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
                self.model.status == LoadTestResultStatus.ACTIVE
            )
        )

    async def filter_by_ids_groped(self, ids: list[int]) -> dict[int, LoadTestResultsModel]:
        results = await self.model.filter(
            self.session,
            order_by=(self.model.id.asc(),),
            clause_filter=(
                self.model.id.in_(ids),
                self.model.status == LoadTestResultStatus.ACTIVE
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
            self.model.status == LoadTestResultStatus.ACTIVE
        )
        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        if end_datetime and start_datetime:
            filters += (self.model.created_at.between(start_datetime, end_datetime),)

        averages = await self.model.averages(
            self.session,
            columns=(
                self.model.average_response_time,
                self.model.total_requests,
                self.model.total_failures,
                self.model.number_of_users,
                self.model.min_response_time,
                self.model.max_response_time,
                self.model.total_requests_per_second,
                self.model.total_failures_per_second
            ),
            clause_filter=filters
        )

        return LoadTestResultsAverages(*averages)


async def get_load_test_results_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> LoadTestResultsRepository:
    return LoadTestResultsRepository(session=session)
