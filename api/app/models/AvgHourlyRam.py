from pydantic import BaseModel
import datetime
class AvgHourlyRam(BaseModel):
    time_stamp: datetime.datetime
    ram_pct:float
    ram_used:float