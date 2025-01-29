from dataclasses import dataclass
from typing import TypedDict

from sqlalchemy import Column, Float
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class ResponseTimesModelDict(TypedDict):
    max_response_time: float
    min_response_time: float
    median_response_time: float
    average_response_time: float


def get_default_response_times_model_dict() -> ResponseTimesModelDict:
    return ResponseTimesModelDict(
        max_response_time=0.0,
        min_response_time=0.0,
        median_response_time=0.0,
        average_response_time=0.0,
    )


@dataclass
class ResponseTimesModelAverages:
    max_response_time: float | None = 0.0
    min_response_time: float | None = 0.0
    median_response_time: float | None = 0.0
    average_response_time: float | None = 0.0


class ResponseTimesModel(MixinModel):
    __abstract__ = True

    max_response_time: Mapped[float] = Column(
        Float,
        name="max_response_time",
        default=0.0,
        nullable=False
    )
    min_response_time: Mapped[float] = Column(
        Float,
        name="min_response_time",
        default=0.0,
        nullable=False
    )
    median_response_time: Mapped[float] = Column(
        Float,
        name="median_response_time",
        default=0.0,
        nullable=False,
    )
    average_response_time: Mapped[float] = Column(
        Float,
        name="average_response_time",
        default=0.0,
        nullable=False
    )

    @classmethod
    def get_average_allowed_columns(cls):
        return (
            cls.max_response_time,
            cls.min_response_time,
            cls.median_response_time,
            cls.average_response_time
        )
