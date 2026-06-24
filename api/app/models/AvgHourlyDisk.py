from pydantic import BaseModel
import datetime
class AvgHourlyDisk(BaseModel):
    time_stamp:datetime.datetime
    disk_pct:float