from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped

from services.postgres.models.ratio_results import RatioResultDict
from utils.clients.postgres.mixin_model import MixinModel


class ScenariosModel(MixinModel):
    __tablename__ = "scenarios"

    name: Mapped[str] = Column(String(100), nullable=False, primary_key=True)
    file: Mapped[str] = Column(String(250), nullable=False)
    ratio_total: Mapped[list[RatioResultDict]] = Column(JSON, nullable=False)
    ratio_per_class: Mapped[list[RatioResultDict]] = Column(JSON, nullable=False)

    service: Mapped[str] = Column(
        String,
        ForeignKey("services.name", ondelete="CASCADE"),
        nullable=False
    )
