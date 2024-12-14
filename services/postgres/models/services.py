from enum import Enum

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class ServiceType(str, Enum):
    INTERNAL = 'INTERNAL'
    PRODUCTION = 'PRODUCTION'


class ServiceStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'


class ServicesModel(MixinModel):
    __tablename__ = "services"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    url: Mapped[str] = Column(String(250), nullable=False)
    type: Mapped[str] = Column(String(50), nullable=False)
    name: Mapped[str] = Column(String(100), nullable=False)
    status: Mapped[str] = Column(String(50), nullable=False, default=ServiceStatus.ACTIVE)
    cluster: Mapped[str] = Column(String(100), nullable=True)
    namespace: Mapped[str] = Column(String(250), nullable=True)
