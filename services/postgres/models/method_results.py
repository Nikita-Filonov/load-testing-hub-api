from datetime import datetime

from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, func, ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel
from utils.common.cache import async_cache


class MethodResultsModel(MixinModel):
    __tablename__ = "method_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    method: Mapped[str] = Column(String(200), nullable=False)
    protocol: Mapped[str] = Column(String(20), nullable=False)
    number_of_requests: Mapped[int] = Column(Integer, nullable=False)
    number_of_failures: Mapped[int] = Column(Integer, nullable=False)
    max_response_time: Mapped[float] = Column(Float, nullable=False)
    min_response_time: Mapped[float] = Column(Float, nullable=False)
    total_response_time: Mapped[float] = Column(Float, nullable=False)
    requests_per_second: Mapped[float] = Column(Float, nullable=False)
    failures_per_second: Mapped[float] = Column(Float, nullable=False)
    average_response_time: Mapped[float] = Column(Float, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

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
    load_test_results_id: Mapped[int] = Column(
        Integer,
        ForeignKey("load_test_results.id", ondelete="CASCADE"),
        nullable=False
    )

    @classmethod
    @async_cache(60 * 60)
    async def get_average_by_method_cached(
            cls,
            session: AsyncSession,
            column: ColumnExpressionArgument,
            method: str,
            scenario: str | None,
    ) -> float:
        filters = (MethodResultsModel.method == method,)
        if scenario:
            filters += (MethodResultsModel.scenario == scenario,)

        result = await cls.average(session, column=column, clause_filter=filters)

        return result or 0.0

    @classmethod
    async def get_average_requests_per_second_cached(
            cls,
            session: AsyncSession,
            method: str,
            scenario: str | None
    ) -> float:
        return await cls.get_average_by_method_cached(
            session,
            column=MethodResultsModel.requests_per_second,
            method=method,
            scenario=scenario
        )

    async def get_average_by_method(
            self,
            session: AsyncSession,
            column: ColumnExpressionArgument,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        filters = (
            MethodResultsModel.method == self.method,
            MethodResultsModel.created_at.between(start_datetime, end_datetime)
        )
        if scenario:
            filters += (MethodResultsModel.scenario == scenario,)

        result = await self.average(session, column=column, clause_filter=filters)

        return result or 0.0

    async def get_average_response_time(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_method(
            session,
            column=MethodResultsModel.average_response_time,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_number_of_requests(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_method(
            session,
            column=MethodResultsModel.number_of_requests,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_requests_per_second(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_method(
            session,
            column=MethodResultsModel.requests_per_second,
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
        return await self.get_average_by_method(
            session,
            column=MethodResultsModel.min_response_time,
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
        return await self.get_average_by_method(
            session,
            column=MethodResultsModel.max_response_time,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_number_of_failures(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_method(
            session,
            column=MethodResultsModel.number_of_failures,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )

    async def get_average_failures_per_second(
            self,
            session: AsyncSession,
            scenario: str | None,
            end_datetime: datetime,
            start_datetime: datetime,
    ) -> float:
        return await self.get_average_by_method(
            session,
            column=MethodResultsModel.failures_per_second,
            scenario=scenario,
            end_datetime=end_datetime,
            start_datetime=start_datetime
        )
