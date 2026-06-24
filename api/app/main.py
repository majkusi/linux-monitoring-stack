from fastapi import FastAPI
from db.connect import Connect
import os
from contextlib import asynccontextmanager
from models.Metric import Metric
from models.AvgHourlyRam import AvgHourlyRam
from models.AvgHourlyCpu import AvgHourlyCpu
from models.AvgHourlyDisk import AvgHourlyDisk
from sql.sql_queries import avg_per_hour
from fastapi import Depends

db = Connect(
    user=os.environ["APP_USER"],
    password=os.environ["APP_USER_PASSWORD"],
    dsn = os.environ["DB_HOST"] + ":" + os.environ["DB_PORT"] + "/" + os.environ["DB_SERVICE"]
)

def get_db():
      return db

@asynccontextmanager
async def lifespan(app:FastAPI):
    get_db().connect()
    yield
    get_db().close()

app = FastAPI(lifespan=lifespan)



@app.get("/metrics", response_model=list[Metric])
async def get_metrics(conn = Depends(get_db)):
    rows = conn.execute("SELECT * FROM METRICS FETCH FIRST 5 ROWS ONLY")
    return [Metric(time_stamp=r[0], 
                   ram_pct=r[1], 
                   ram_used=r[2], 
                   ram_total=r[3], 
                   disk_pct=r[4], 
                   cpu_pct=r[5]) 
                   for r in rows]

@app.get("/metrics/average/hourly/ram",response_model=list[AvgHourlyRam])
async def get_hourly_ram(conn = Depends(get_db)):
        avg = conn.execute(avg_per_hour(["RAM_PCT","RAM_USED"]))
        result = []
        for record in avg:
              result.append(AvgHourlyRam(time_stamp=record[0],ram_pct=record[1],ram_used=record[2]))
        return result

@app.get("/metrics/average/hourly/cpu",response_model=list[AvgHourlyCpu])
async def get_avg_hourly_cpu(conn = Depends(get_db)):
        avg = conn.execute(avg_per_hour(["CPU_PCT"]))
        result = []
        for record in avg:
              result.append(AvgHourlyCpu(time_stamp=record[0],cpu_pct=record[1]))
        return result

@app.get("/metrics/average/hourly/disk", response_model=list[AvgHourlyDisk])
async def get_avg_hourly_disk(conn = Depends(get_db)):
      avg = conn.execute(avg_per_hour(["DISK_PCT"]))
      result = []
      for record in avg:
            result.append(AvgHourlyDisk(time_stamp=record[0],disk_pct=record[1]))
      return result