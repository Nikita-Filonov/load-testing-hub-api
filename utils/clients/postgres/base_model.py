from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()


class Base(DeclarativeBase):
    pass
