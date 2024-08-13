from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class ServicesModel(MixinModel):
    __tablename__ = "services"

    url: Mapped[str] = Column(String(250), nullable=False)
    name: Mapped[str] = Column(String(100), nullable=False, primary_key=True)
    cluster: Mapped[str] = Column(String(100), nullable=True)
    namespace: Mapped[str] = Column(String(250), nullable=True)
    is_internal: Mapped[bool] = Column(Boolean, nullable=False, server_default='false')
