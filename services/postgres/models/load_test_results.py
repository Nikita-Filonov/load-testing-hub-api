from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from services.postgres.models.base.metrics import MetricsModel
from services.postgres.models.base.number_of_users import NumberOfUsersModel
from services.postgres.models.base.status import StatusModel

if TYPE_CHECKING:
    from services.postgres.models import ScenariosModel, ServicesModel


class LoadTestResultsModel(MetricsModel, NumberOfUsersModel, StatusModel):
    __tablename__ = "load_test_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    comment: Mapped[str | None] = Column(String(length=250), nullable=True)
    trigger_ci_job_url: Mapped[str | None] = Column(String, nullable=True)
    trigger_ci_pipeline_url: Mapped[str | None] = Column(String, nullable=True)
    trigger_ci_project_version: Mapped[str | None] = Column(String, nullable=True)
    load_tests_ci_job_url: Mapped[str | None] = Column(String, nullable=True)
    load_tests_ci_pipeline_url: Mapped[str | None] = Column(String, nullable=True)
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

    @classmethod
    def get_average_allowed_columns(cls):
        return (
            *MetricsModel.get_average_allowed_columns(),
            *NumberOfUsersModel.get_average_allowed_columns()
        )
