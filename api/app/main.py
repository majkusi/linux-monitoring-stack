from fastapi import FastAPI
import oracledb
import os

from models.Metric import Metric

db_user = os.environ["APP_USER"]
db_user_password = os.environ["APP_USER_PASSWORD"]
db_port = os.environ["DB_PORT"]
db_host = os.environ["DB_HOST"]
db_service = os.environ["DB_SERVICE"]
db_dsn = db_host + ":" + db_port + "/" + db_service

pool = oracledb.create_pool(user=db_user,password=db_user_password,dsn=db_dsn)

app = FastAPI()



@app.get("/metrics", response_model=list[Metric])
async def get_metrics():
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM METRICS FETCH FIRST 5 ROWS ONLY;")
            result = cursor.fetchall()
            final_list = []
            for entry in result:
                metric = Metric(time_stamp=entry[0], 
                       ram_pct=entry[1],
                       ram_used=entry[2],
                       ram_total=entry[3],
                       disk_pct=entry[4],
                       cpu_pct=entry[5])
                final_list.append(metric)
            return final_list;
