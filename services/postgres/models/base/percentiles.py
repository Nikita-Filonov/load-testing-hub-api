from dataclasses import dataclass
from typing import TypedDict

from sqlalchemy import Column, Float
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class PercentilesModelDict(TypedDict):
    response_time_percentile_50: float
    response_time_percentile_60: float
    response_time_percentile_70: float
    response_time_percentile_80: float
    response_time_percentile_90: float
    response_time_percentile_95: float
    response_time_percentile_99: float
    response_time_percentile_100: float


def get_default_percentiles_model_dict() -> PercentilesModelDict:
    return PercentilesModelDict(
        response_time_percentile_50=0.0,
        response_time_percentile_60=0.0,
        response_time_percentile_70=0.0,
        response_time_percentile_80=0.0,
        response_time_percentile_90=0.0,
        response_time_percentile_95=0.0,
        response_time_percentile_99=0.0,
        response_time_percentile_100=0.0,
    )


@dataclass
class PercentilesModelAverages:
    response_time_percentile_50: float | None = 0.0
    response_time_percentile_60: float | None = 0.0
    response_time_percentile_70: float | None = 0.0
    response_time_percentile_80: float | None = 0.0
    response_time_percentile_90: float | None = 0.0
    response_time_percentile_95: float | None = 0.0
    response_time_percentile_99: float | None = 0.0
    response_time_percentile_100: float | None = 0.0


class PercentilesModel(MixinModel):
    __abstract__ = True

    response_time_percentile_50: Mapped[float] = Column(
        Float,
        name="response_time_percentile_50",
        default=0.0,
        nullable=False,
    )
    response_time_percentile_60: Mapped[float] = Column(
        Float,
        name="response_time_percentile_60",
        default=0.0,
        nullable=False,
    )
    response_time_percentile_70: Mapped[float] = Column(
        Float,
        name="response_time_percentile_70",
        default=0.0,
        nullable=False,
    )
    response_time_percentile_80: Mapped[float] = Column(
        Float,
        name="response_time_percentile_80",
        default=0.0,
        nullable=False,
    )
    response_time_percentile_90: Mapped[float] = Column(
        Float,
        name="response_time_percentile_90",
        default=0.0,
        nullable=False,
    )
    response_time_percentile_95: Mapped[float] = Column(
        Float,
        name="response_time_percentile_95",
        default=0.0,
        nullable=False,
    )
    response_time_percentile_99: Mapped[float] = Column(
        Float,
        name="response_time_percentile_99",
        default=0.0,
        nullable=False,
    )
    response_time_percentile_100: Mapped[float] = Column(
        Float,
        name="response_time_percentile_100",
        default=0.0,
        nullable=False,
    )

    @classmethod
    def get_average_allowed_columns(cls):
        return (
            cls.response_time_percentile_50,
            cls.response_time_percentile_60,
            cls.response_time_percentile_70,
            cls.response_time_percentile_80,
            cls.response_time_percentile_90,
            cls.response_time_percentile_95,
            cls.response_time_percentile_99,
            cls.response_time_percentile_100,
        )
