from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import Mapped

from services.postgres.models.base.status import StatusModel


class IntegrationsModel(StatusModel):
    __tablename__ = "integrations"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    system_type: Mapped[str] = Column(String(30), nullable=False)
    order_index: Mapped[int] = Column(Integer, nullable=False)
    url_template: Mapped[str] = Column(Text, nullable=False)
    environment_type: Mapped[str] = Column(String(30), nullable=False)

    service_id: Mapped[int] = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
    )

    def get_ready_url(
            self,
            host: str,
            to_time: str | None = None,
            from_time: str | None = name
    ) -> str:
        return self.url_template.format(host=host, to_time=to_time, from_time=from_time)
