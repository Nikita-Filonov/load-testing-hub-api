from dataclasses import dataclass
from typing import TypedDict

from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class NumberOfUsersModelDict(TypedDict):
    number_of_users: int


def get_default_number_of_users_model_dict() -> NumberOfUsersModelDict:
    return NumberOfUsersModelDict(number_of_users=0)


@dataclass
class NumberOfUsersModelAverages:
    number_of_users: float | None = 0.0


class NumberOfUsersModel(MixinModel):
    __abstract__ = True

    number_of_users: Mapped[int] = Column(
        Integer,
        name="number_of_users",
        default=0,
        nullable=False
    )

    @classmethod
    def get_average_allowed_columns(cls):
        return (cls.number_of_users,)
