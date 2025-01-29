from dataclasses import dataclass
from typing import TypedDict

from sqlalchemy import Column, Float
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class RequestsPerSecondModelDict(TypedDict):
    requests_per_second: float
    failures_per_second: float


def get_default_requests_per_second_model_dict() -> RequestsPerSecondModelDict:
    return RequestsPerSecondModelDict(
        requests_per_second=0.0,
        failures_per_second=0.0
    )


@dataclass
class RequestsPerSecondModelAverages:
    requests_per_second: float | None = 0.0
    failures_per_second: float | None = 0.0


class RequestsPerSecondModel(MixinModel):
    __abstract__ = True

    requests_per_second: Mapped[float] = Column(
        Float,
        name="requests_per_second",
        default=0.0,
        nullable=False
    )
    failures_per_second: Mapped[float] = Column(
        Float,
        name="failures_per_second",
        default=0.0,
        nullable=False,
    )

    @classmethod
    def get_average_allowed_columns(cls):
        return (
            cls.requests_per_second,
            cls.failures_per_second
        )
