from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, func, ForeignKey, ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel
from utils.common.cache import async_cache


class LoadTestResultsModel(MixinModel):
    __tablename__ = "load_test_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    trigger_ci_pipeline_url: Mapped[str | None] = Column(String, nullable=True)
    trigger_ci_project_title: Mapped[str | None] = Column(String, nullable=True)
    trigger_ci_project_version: Mapped[str | None] = Column(String, nullable=True)
    load_tests_ci_pipeline_url: Mapped[str | None] = Column(String, nullable=True)
    number_of_users: Mapped[int] = Column(Integer, nullable=False)
    total_requests: Mapped[int] = Column(Integer, nullable=False)
    total_failures: Mapped[int] = Column(Integer, nullable=False)
    max_response_time: Mapped[float] = Column(Float, nullable=False)
    min_response_time: Mapped[float] = Column(Float, nullable=False)
    average_response_time: Mapped[float] = Column(Float, nullable=False)
    total_requests_per_second: Mapped[float] = Column(Float, nullable=False)
    total_failures_per_second: Mapped[float] = Column(Float, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    started_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)

    service: Mapped[str] = Column(
        String,
        ForeignKey("services.name", ondelete="CASCADE"),
        nullable=False
    )
    scenario: Mapped[str] = Column(
        String,
        ForeignKey("scenarios.name", ondelete="CASCADE"),
        nullable=True
    )

    @classmethod
    @async_cache(60 * 60)
    async def get_average_total_requests_per_second_cached(
            cls,
            session: AsyncSession,
            service: str,
            scenario: str | None,
    ) -> float:
        filters = (LoadTestResultsModel.service == service,)
        if scenario:
            filters += (LoadTestResultsModel.scenario == scenario,)

        result = await cls.average(
            session,
            column=LoadTestResultsModel.total_requests_per_second,
            clause_filter=filters
        )

        return result or 0.0

    async def get_average_by_service(
            self,
            session: AsyncSession,
            column: ColumnExpressionArgument,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        filters = (
            LoadTestResultsModel.service == self.service,
            LoadTestResultsModel.created_at.between(start_datetime, end_datetime)
        )
        if scenario:
            filters += (LoadTestResultsModel.scenario == scenario,)

        result = await self.average(session, column=column, clause_filter=filters)

        return result or 0.0

    async def get_average_number_of_users(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_service(
            session,
            column=LoadTestResultsModel.number_of_users,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_total_requests(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_service(
            session,
            column=LoadTestResultsModel.total_requests,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_total_failures(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_service(
            session,
            column=LoadTestResultsModel.total_failures,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_total_requests_per_second(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_service(
            session,
            column=LoadTestResultsModel.total_requests_per_second,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_total_failures_per_second(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_service(
            session,
            column=LoadTestResultsModel.total_failures_per_second,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_max_response_time(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_service(
            session,
            column=LoadTestResultsModel.max_response_time,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_min_response_time(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_service(
            session,
            column=LoadTestResultsModel.min_response_time,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_response_time(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_service(
            session,
            column=LoadTestResultsModel.average_response_time,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )
