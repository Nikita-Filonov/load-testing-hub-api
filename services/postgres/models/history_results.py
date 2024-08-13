from datetime import datetime

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class HistoryResultsModel(MixinModel):
    __tablename__ = "history_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    datetime: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    number_of_users: Mapped[int] = Column(Integer, nullable=False)
    requests_per_second: Mapped[float] = Column(Float, nullable=False)
    failures_per_second: Mapped[float] = Column(Float, nullable=False)
    average_response_time: Mapped[float] = Column(Float, nullable=False)
    response_time_percentile_95: Mapped[float] = Column(Float, nullable=False)

    load_test_results_id: Mapped[int] = Column(
        Integer,
        ForeignKey("load_test_results.id", ondelete="CASCADE"),
        nullable=False
    )
