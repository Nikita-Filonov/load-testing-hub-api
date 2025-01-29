from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped

from services.postgres.models.base.content_length import ContentLengthModel
from services.postgres.models.base.datetime import DatetimeModel
from services.postgres.models.base.metrics import MetricsModel
from services.postgres.models.base.number_of_users import NumberOfUsersModel


class MethodResultsHistoryModel(
    MetricsModel,
    DatetimeModel,
    NumberOfUsersModel,
    ContentLengthModel
):
    __tablename__ = "method_results_history"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    method_result_id: Mapped[int] = Column(
        Integer,
        ForeignKey("method_results.id", ondelete="CASCADE"),
        nullable=False
    )
