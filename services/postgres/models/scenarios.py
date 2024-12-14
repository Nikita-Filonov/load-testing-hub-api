from enum import Enum

from sqlalchemy import Column, String, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped

from services.postgres.models.ratio_results import RatioResultDict
from utils.clients.postgres.mixin_model import MixinModel


class ScenarioStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'


class ScenariosModel(MixinModel):
    __tablename__ = "scenarios"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    tags: Mapped[list[str]] = Column(JSON, nullable=False, default=[])
    name: Mapped[str] = Column(String(100), nullable=False)
    file: Mapped[str] = Column(String(250), nullable=False)
    status: Mapped[str] = Column(String(50), nullable=False, default=ScenarioStatus.ACTIVE)
    version: Mapped[str] = Column(String(50), nullable=False)
    ratio_total: Mapped[list[RatioResultDict]] = Column(JSON, nullable=False, default=[])
    ratio_per_class: Mapped[list[RatioResultDict]] = Column(JSON, nullable=False, default=[])

    service_id: Mapped[int] = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False
    )
