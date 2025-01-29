from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class ModelStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'


class StatusModel(MixinModel):
    __abstract__ = True

    status: Mapped[str] = Column(String(50), nullable=False, default=ModelStatus.ACTIVE)
