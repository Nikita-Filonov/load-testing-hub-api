from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship

from utils.clients.postgres.mixin_model import MixinModel

if TYPE_CHECKING:
    from services.postgres.models import ServicesModel


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
    average_content_length: Mapped[float] = Column(Float, nullable=False)
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
