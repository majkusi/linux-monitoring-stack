from pydantic import BaseModel
import datetime
class AvgHourlyCpu(BaseModel):
    time_stamp:datetime.datetime
    cpu_pct:float