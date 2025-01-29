from sqlalchemy import Column, String, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped

from services.postgres.models.base.status import StatusModel
from services.postgres.models.ratio_results import RatioResultDict


class ScenariosModel(StatusModel):
    __tablename__ = "scenarios"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    tags: Mapped[list[str]] = Column(JSON, nullable=False, default=[])
    name: Mapped[str] = Column(String(100), nullable=False)
    file: Mapped[str] = Column(String(250), nullable=False)
    version: Mapped[str] = Column(String(50), nullable=False)
    ratio_total: Mapped[list[RatioResultDict]] = Column(JSON, nullable=False, default=[])
    ratio_per_class: Mapped[list[RatioResultDict]] = Column(JSON, nullable=False, default=[])
    number_of_users: Mapped[int] = Column(Integer, nullable=False, default=0)
    runtime_duration: Mapped[str] = Column(String(50), nullable=False, default='0s')

    service_id: Mapped[int] = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False
    )
