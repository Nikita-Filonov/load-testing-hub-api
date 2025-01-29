from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship

from services.postgres.models.base.content_length import ContentLengthModel
from services.postgres.models.base.metrics import MetricsModel
from services.postgres.models.base.status import StatusModel
from utils.base.strings import get_short_method

if TYPE_CHECKING:
    from services.postgres.models import ServicesModel, LoadTestResultsModel


class MethodResultsModel(MetricsModel, ContentLengthModel, StatusModel):
    __tablename__ = "method_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    method: Mapped[str] = Column(String(200), nullable=False)
    protocol: Mapped[str] = Column(String(20), nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

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

    load_test_result_id: Mapped[int] = Column(
        Integer,
        ForeignKey("load_test_results.id", ondelete="CASCADE"),
        nullable=False
    )
    load_test_result: Mapped["LoadTestResultsModel"] = relationship("LoadTestResultsModel")

    def get_compare_title(self) -> str:
        return f"{self.load_test_result.get_compare_title()}: {get_short_method(self.method)}"

    @classmethod
    def get_average_allowed_columns(cls):
        return (
            *MetricsModel.get_average_allowed_columns(),
            *ContentLengthModel.get_average_allowed_columns()
        )
