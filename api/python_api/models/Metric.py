import datetime
from pydantic import BaseModel

class Metric(BaseModel):
    time_stamp: datetime.datetime
    ram_pct: float
    ram_used: float
    ram_total: float
    disk_pct: float
    cpu_pct: float