from pydantic import BaseModel

class AvgHourlyDisk(BaseModel):
    disk_pct:float