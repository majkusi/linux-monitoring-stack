from fastapi import FastAPI
from db.connect import Connect
import os
from contextlib import asynccontextmanager
from models.Metric import Metric

db = Connect(
    user=os.environ["APP_USER"],
    password=os.environ["APP_USER_PASSWORD"],
    dsn = os.environ["DB_HOST"] + ":" + os.environ["DB_PORT"] + "/" + os.environ["DB_SERVICE"]
)
app = FastAPI()


@asynccontextmanager
async def lifespan(app:FastAPI):
    db.connect()
    yield
    db.close()


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
