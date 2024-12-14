from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, Float, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from utils.clients.postgres.mixin_model import MixinModel

if TYPE_CHECKING:
    from services.postgres.models import ScenariosModel, ServicesModel


class LoadTestResultStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'


class LoadTestResultsModel(MixinModel):
    __tablename__ = "load_test_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    status: Mapped[str] = Column(String(50), nullable=False, default=LoadTestResultStatus.ACTIVE)
    comment: Mapped[str | None] = Column(String(length=250), nullable=True)
    trigger_ci_job_url: Mapped[str | None] = Column(String, nullable=True)
    trigger_ci_pipeline_url: Mapped[str | None] = Column(String, nullable=True)
    trigger_ci_project_version: Mapped[str | None] = Column(String, nullable=True)
    load_tests_ci_job_url: Mapped[str | None] = Column(String, nullable=True)
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

    service_id: Mapped[int] = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False
    )
    service: Mapped["ServicesModel"] = relationship("ServicesModel")

    scenario_id: Mapped[int] = Column(
        Integer,
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False
    )
    scenario: Mapped["ScenariosModel"] = relationship("ScenariosModel")

    def get_compare_title(self) -> str:
        return self.trigger_ci_project_version or f'#{self.id}'
