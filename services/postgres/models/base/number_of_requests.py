from dataclasses import dataclass
from typing import TypedDict

from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class NumberOfRequestsModelDict(TypedDict):
    number_of_requests: int
    number_of_failures: int


def get_default_number_of_requests_model_dict() -> NumberOfRequestsModelDict:
    return NumberOfRequestsModelDict(
        number_of_requests=0,
        number_of_failures=0
    )


@dataclass
class NumberOfRequestsModelAverages:
    number_of_requests: float | None = 0.0
    number_of_failures: float | None = 0.0


class NumberOfRequestsModel(MixinModel):
    __abstract__ = True

    number_of_requests: Mapped[int] = Column(
        Integer,
        name="number_of_requests",
        default=0,
        nullable=False,
    )
    number_of_failures: Mapped[int] = Column(
        Integer,
        name="number_of_failures",
        default=0,
        nullable=False
    )

    @classmethod
    def get_average_allowed_columns(cls):
        return (
            cls.number_of_requests,
            cls.number_of_failures
        )
