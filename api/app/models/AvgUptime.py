from pydantic import BaseModel
class AvgUptime(BaseModel):
    successes:int
    total:int
    uptime_pct:float
