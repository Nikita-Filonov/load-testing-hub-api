from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()


class Base(DeclarativeBase):
    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
