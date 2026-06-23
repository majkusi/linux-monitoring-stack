from pydantic import BaseModel

class AvgHourlyCpu(BaseModel):
    cpu_pct:float