import datetime
from pydantic import BaseModel

class Metric(BaseModel):
    time_stamp: datetime.datetime
    http_status: int