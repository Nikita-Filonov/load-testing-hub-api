from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class ExceptionResultsModel(MixinModel):
    __tablename__ = "exception_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    message: Mapped[str] = Column(Text, nullable=False)
    details: Mapped[str] = Column(Text, nullable=False)
    number_of_exceptions: Mapped[int] = Column(Integer, nullable=False)

    load_test_result_id: Mapped[int] = Column(
        Integer,
        ForeignKey("load_test_results.id", ondelete="CASCADE"),
        nullable=False
    )
