import asyncio
from datetime import datetime
from itertools import groupby, zip_longest
from typing import Sequence, Annotated, NamedTuple, TypedDict

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from services.postgres.client import get_postgres_session
from services.postgres.models import MethodResultsModel
from services.postgres.models.method_results import MethodResultStatus
from utils.clients.postgres.repository import BasePostgresRepository


class MethodResultsAverages(NamedTuple):
    response_time: float | None
    content_length: float | None
    min_response_time: float | None
    max_response_time: float | None
    number_of_requests: float | None
    number_of_failures: float | None
    requests_per_second: float | None
    failures_per_second: float | None


class CreateMethodResultsModelDict(TypedDict):
    method: str
    protocol: str
    number_of_requests: int
    number_of_failures: int
    max_response_time: float
    min_response_time: float
    total_response_time: float
    requests_per_second: float
    failures_per_second: float
    average_response_time: float
    average_content_length: float
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
            self.session, clause_filter=filters, status=MethodResultStatus.DELETED
        )

    async def create_multiple(self, data: list[CreateMethodResultsModelDict]):
        await self.model.bulk_create(self.session, data)

    async def filter(
            self,
            method: str | None = None,
            service_id: str | None = None,
            scenario_id: int | None = None,
            end_datetime: datetime | None = None,
            start_datetime: datetime | None = None
    ):
        filters = (self.model.status == MethodResultStatus.ACTIVE,)
        if method:
            filters += (self.model.method == method,)

        if service_id:
            filters += (self.model.service_id == service_id,)

        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        if end_datetime and start_datetime:
            filters += (self.model.created_at.between(start_datetime, end_datetime),)

        return await self.model.filter(self.session, clause_filter=filters)

    async def filter_with_distinct_by_method(
            self,
            service_id: int,
            method: str | None = None,
            scenario_id: int | None = None,
    ) -> Sequence[MethodResultsModel]:
        filters = (
            self.model.status == MethodResultStatus.ACTIVE,
            self.model.service_id == service_id,
        )
        if method:
            filters += (func.lower(self.model.method).contains(method.lower()),)

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
                self.model.status == MethodResultStatus.ACTIVE,
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
                self.model.status == MethodResultStatus.ACTIVE,
                self.model.load_test_result_id.in_(load_test_result_ids),
            )
        )

        return {
            load_test_result_id: list(results)
            for load_test_result_id, results
            in groupby(results, key=lambda r: r.load_test_result_id)
        }

    async def get_averages(
            self,
            method: str,
            service_id: int,
            scenario_id: int | None = None,
            end_datetime: datetime | None = None,
            start_datetime: datetime | None = None
    ) -> MethodResultsAverages:
        filters = (
            self.model.status == MethodResultStatus.ACTIVE,
            self.model.method == method,
            self.model.service_id == service_id
        )
        if scenario_id:
            filters += (self.model.scenario_id == scenario_id,)

        if end_datetime and start_datetime:
            filters += (self.model.created_at.between(start_datetime, end_datetime),)

        averages = await self.model.averages(
            self.session,
            columns=(
                self.model.average_response_time,
                self.model.average_content_length,
                self.model.min_response_time,
                self.model.max_response_time,
                self.model.number_of_requests,
                self.model.number_of_failures,
                self.model.requests_per_second,
                self.model.failures_per_second
            ),
            clause_filter=filters
        )

        return MethodResultsAverages(*averages)

    async def get_averages_for_methods(
            self,
            methods: list[str],
            service_id: int,
            scenario_id: int | None = None,
            end_datetime: datetime | None = None,
            start_datetime: datetime | None = None
    ) -> dict[str, MethodResultsAverages]:
        results = await asyncio.gather(*[
            self.get_averages(method, service_id, scenario_id, end_datetime, start_datetime)
            for method in methods
        ])

        return {method: averages for method, averages in zip_longest(methods, results)}


async def get_method_results_repository(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
) -> MethodResultsRepository:
    return MethodResultsRepository(session=session)
