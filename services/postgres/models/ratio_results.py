from typing import TypedDict

from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class RatioResultDict(TypedDict):
    name: str
    ratio: float
    tasks: list['RatioResultDict']


class RatioResultsModel(MixinModel):
    __tablename__ = "ratio_results"

    ratio_total: Mapped[list[RatioResultDict]] = Column(JSON, nullable=False)
    ratio_per_class: Mapped[list[RatioResultDict]] = Column(JSON, nullable=False)

    load_test_results_id: Mapped[int] = Column(
        Integer,
        ForeignKey("load_test_results.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )
