from pydantic import BaseModel

class AvgHourlyRam(BaseModel):
    ram_pct:float
    ram_used:float