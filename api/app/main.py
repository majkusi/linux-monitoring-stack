from fastapi import FastAPI
from db.connect import Connect
import os
from contextlib import asynccontextmanager
from models.Metric import Metric
from models.AvgHourlyRam import AvgHourlyRam
from models.AvgHourlyCpu import AvgHourlyCpu
from models.AvgHourlyDisk import AvgHourlyDisk
from sql.sql_queries import avg_per_hour

db = Connect(
    user=os.environ["APP_USER"],
    password=os.environ["APP_USER_PASSWORD"],
    dsn = os.environ["DB_HOST"] + ":" + os.environ["DB_PORT"] + "/" + os.environ["DB_SERVICE"]
)

@asynccontextmanager
async def lifespan(app:FastAPI):
    db.connect()
    yield
    db.close()

app = FastAPI(lifespan=lifespan)

@app.get("/metrics", response_model=list[Metric])
async def get_metrics():
    rows = db.execute("SELECT * FROM METRICS FETCH FIRST 5 ROWS ONLY")
    return [Metric(time_stamp=r[0], 
                   ram_pct=r[1], 
                   ram_used=r[2], 
                   ram_total=r[3], 
                   disk_pct=r[4], 
                   cpu_pct=r[5]) 
                   for r in rows]

@app.get("/metrics/average/hourly/ram",response_model=AvgHourlyRam)
async def get_hourly_ram():
        avg = db.execute(avg_per_hour(["RAM_PCT","RAM_USED"]))
        return AvgHourlyRam(time_stamp=avg[0][0],ram_pct=avg[0][1],ram_used=avg[0][2])

@app.get("/metrics/average/hourly/cpu",response_model=AvgHourlyCpu)
async def get_avg_hourly_cpu():
        avg = db.execute(avg_per_hour(["CPU_PCT"]))
        return AvgHourlyCpu(time_stamp=avg[0][0],cpu_pct=avg[0][1])

@app.get("/metrics/average/hourly/disk", response_model=AvgHourlyDisk)
async def get_avg_hourly_disk():
      avg = db.execute(avg_per_hour(["DISK_PCT"]))
      return AvgHourlyDisk(time_stamp=avg[0][0],disk_pct=avg[0][1])