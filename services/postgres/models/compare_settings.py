from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class CompareSettingsModel(MixinModel):
    __tablename__ = "compare_settings"

    response_time_weight: Mapped[float] = Column(Float, nullable=False, default=0.5)
    min_response_time_weight: Mapped[float] = Column(Float, nullable=False, default=0.0)
    max_response_time_weight: Mapped[float] = Column(Float, nullable=False, default=0.0)
    number_of_requests_weight: Mapped[float] = Column(Float, nullable=False, default=0.0)
    number_of_failures_weight: Mapped[float] = Column(Float, nullable=False, default=0.0)
    requests_per_second_weight: Mapped[float] = Column(Float, nullable=False, default=0.5)
    failures_per_second_weight: Mapped[float] = Column(Float, nullable=False, default=0.0)

    service_id: Mapped[int] = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )
