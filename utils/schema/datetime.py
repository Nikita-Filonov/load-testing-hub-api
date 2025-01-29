from datetime import datetime

from pydantic import BaseModel


class DatetimeSchema(BaseModel):
    datetime: datetime
