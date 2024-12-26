from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class IntegrationStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'


class IntegrationEnvironmentType(str, Enum):
    INTERNAL = 'INTERNAL'
    PRODUCTION = 'PRODUCTION'


class IntegrationsModel(MixinModel):
    __tablename__ = "integrations"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    status: Mapped[str] = Column(String(50), nullable=False, default=IntegrationStatus.ACTIVE)
    cluster: Mapped[str] = Column(String(100), nullable=False)
    namespace: Mapped[str] = Column(String(250), nullable=False)
    environment_type: Mapped[str] = Column(String(30), nullable=False)

    service_id: Mapped[int] = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,

    )
