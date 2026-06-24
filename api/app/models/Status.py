import datetime
from pydantic import BaseModel

class Status(BaseModel):
    time_stamp: datetime.datetime
    http_status: int