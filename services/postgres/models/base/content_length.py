from dataclasses import dataclass
from typing import TypedDict

from sqlalchemy import Column, Float
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class ContentLengthModelDict(TypedDict):
    average_content_length: float


def get_default_content_length_model_dict() -> ContentLengthModelDict:
    return ContentLengthModelDict(average_content_length=0.0)


@dataclass
class ContentLengthModelAverages:
    average_content_length: float | None = 0.0


class ContentLengthModel(MixinModel):
    __abstract__ = True

    average_content_length: Mapped[float] = Column(
        Float,
        name="average_content_length",
        default=0.0,
        nullable=False,
    )

    @classmethod
    def get_average_allowed_columns(cls):
        return (cls.average_content_length,)
