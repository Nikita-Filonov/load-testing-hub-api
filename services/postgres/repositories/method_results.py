import asyncio
from dataclasses import dataclass
from datetime import datetime
from itertools import groupby, zip_longest
from typing import Sequence, Annotated

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from services.postgres.client import get_postgres_session
from services.postgres.models import MethodResultsModel
from services.postgres.models.base.content_length import ContentLengthModelAverages, ContentLengthModelDict
from services.postgres.models.base.metrics import MetricsModelAverages, MetricsModelDict
from services.postgres.models.base.status import ModelStatus
from utils.clients.postgres.repository import BasePostgresRepository


@dataclass
class MethodResultsAverages(MetricsModelAverages, ContentLengthModelAverages):
    ...


class CreateMethodResultsModelDict(MetricsModelDict, ContentLengthModelDict):
    method: str
    protocol: str
    created_at: datetime

    service_id: int
    scenario_id: int
    load_test_result_id: int


class MethodResultsRepository(BasePostgresRepository):
    model = MethodResultsModel

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
            filters += (self.model.load_test_result_id == load_test_result_id,)

        if not filters:
            return

        await self.model.update(
            self.session, clause_filter=filters, status=ModelStatus.DELETED
        )

    async def create_multiple(self, data: list[dict]):
        await self.model.bulk_create(self.session, data)

    async def filter(
            self,
            method: str | None = None,
            service_id: int | None = None,
            scenario_id: int | None = None,
            end_datetime: datetime | None = None,
            start_datetime: datetime | None = None
    ):
        filters = (self.model.status == ModelStatus.ACTIVE,)
        if method:
            filters += (self.model.method == method,)

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

    async def filter_groped_by_id(
            self,
            method: str | None = None,
            load_test_result_ids: list[int] | None = None
    ) -> dict[int, MethodResultsModel]:
        filters = (self.model.status == ModelStatus.ACTIVE,)
        if method:
            filters += (self.model.method == method,)

        if load_test_result_ids:
            filters += (self.model.load_test_result_id.in_(load_test_result_ids),)

        results = await self.model.filter(
            self.session,
            options=(joinedload(self.model.load_test_result),),
            order_by=(self.model.id,),
            clause_filter=filters
        )

        return {result.id: result for result in results}

    async def filter_with_distinct_by_method(
            self,
            service_id: int,
            method: str | None = None,
            protocol: str | None = None,
            scenario_id: int | None = None,
    ) -> Sequence[MethodResultsModel]:
        filters = (
            self.model.status == ModelStatus.ACTIVE,
            self.model.service_id == service_id,
        )
        if method:
            filters += (func.lower(self.model.method).contains(method.lower()),)

        if protocol:
            filters += (self.model.protocol == protocol,)

        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        return await self.model.filter(
            self.session, distinct=(self.model.method,), clause_filter=filters
        )

    async def filter_by_load_test_result_id(self, load_test_result_id: int) -> Sequence[MethodResultsModel]:
        return await self.model.filter(
            self.session,
            order_by=(self.model.method,),
            clause_filter=(
                self.model.status == ModelStatus.ACTIVE,
                self.model.load_test_result_id == load_test_result_id,
            )
        )

    async def filter_by_load_test_result_ids_groped(
            self,
            load_test_result_ids: list[int]
    ) -> dict[int, Sequence[MethodResultsModel]]:
        results = await self.model.filter(
            self.session,
            order_by=(self.model.load_test_result_id,),
            clause_filter=(
                self.model.status == ModelStatus.ACTIVE,
                self.model.load_test_result_id.in_(load_test_result_ids),
            )
        )

        return {
            load_test_result_id: list(results)
            for load_test_result_id, results
            in groupby(results, key=lambda r: r.load_test_result_id)
        }

    async def get_by_id(self, method_result_id: int) -> MethodResultsModel | None:
        return await self.model.get(
            self.session,
            clause_filter=(
                self.model.id == method_result_id,
                self.model.status == ModelStatus.ACTIVE
            )
        )

    async def get_by_method(
            self,
            method: str,
            load_test_result_id: int | None = None
    ) -> MethodResultsModel | None:
        filters = (
            self.model.method == method,
            self.model.status == ModelStatus.ACTIVE,
        )
        if load_test_result_id:
            filters += (self.model.load_test_result_id == load_test_result_id,)

        return await self.model.get(self.session, clause_filter=filters)

    async def get_previous(
            self,
            method: str,
            service_id: int,
            scenario_id: int | None,
            method_result_id: int
    ) -> MethodResultsModel | None:
        filters = (
            self.model.id < method_result_id,
            self.model.method == method,
            self.model.status == ModelStatus.ACTIVE,
            self.model.service_id == service_id
        )
        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        previous_results = await self.model.filter(
            self.session, limit=1, order_by=(self.model.id.desc(),), clause_filter=filters
        )

        return previous_results[0] if len(previous_results) > 0 else None

    async def get_averages(
            self,
            method: str,
            service_id: int,
            scenario_id: int | None = None,
            end_datetime: datetime | None = None,
            start_datetime: datetime | None = None
    ) -> MethodResultsAverages:
        filters = (
            self.model.status == ModelStatus.ACTIVE,
            self.model.method == method,
            self.model.service_id == service_id
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

        return MethodResultsAverages(**averages)

    async def get_averages_for_method_results(
            self,
            results: Sequence[MethodResultsModel],
            service_id: int,
            scenario_id: int | None = None,
            end_datetime: datetime | None = None,
            start_datetime: datetime | None = None
    ) -> dict[MethodResultsModel, MethodResultsAverages]:
        average_results = await asyncio.gather(*[
            self.get_averages(result.method, service_id, scenario_id, end_datetime, start_datetime)
            for result in results
        ])

        return {result: averages for result, averages in zip_longest(results, average_results)}


async def get_method_results_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> MethodResultsRepository:
    return MethodResultsRepository(session=session)
