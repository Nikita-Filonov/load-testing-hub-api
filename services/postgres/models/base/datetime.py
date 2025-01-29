from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class DatetimeModelDict(TypedDict):
    datetime: datetime


class DatetimeModel(MixinModel):
    __abstract__ = True

    datetime: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
