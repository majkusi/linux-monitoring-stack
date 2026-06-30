import oracledb
import os
import time
import datetime

db_user = os.environ["APP_USER"]
db_user_password = os.environ["APP_USER_PASSWORD"]
db_port = os.environ["DB_PORT"]
db_host = os.environ["DB_HOST"]
db_service = os.environ["DB_SERVICE"]
dsn = db_host + ":" + db_port + "/" + db_service

def insert_into_db(connection, cursor, max_ts, input_file):
    try:
        with open(input_file,"r") as file:
            for line in file:
                fields = line.strip().split(",")
                ts = datetime.datetime.strptime(fields[0],"%Y-%m-%d %H:%M:%S")
                if "health" in input_file:
                    if ts > max_ts:
                        cursor.execute(
                                    "INSERT INTO METRICS (TIME_STAMP, RAM_PCT, RAM_USED, RAM_TOTAL, DISK_PCT, CPU_PCT) " \
                                    "VALUES (:1, :2, :3, :4, :5, :6)",
                                    [ts, fields[1], fields[2], fields[3], fields[4], fields[5]])
                elif "service" in input_file:
                    if ts > max_ts:
                        cursor.execute(
                                    "INSERT INTO STATUS (TIME_STAMP, HTTP_STATUS, MTLS_NO_CERT, MTLS_CERT )" \
                                    "VALUES (:1, :2, :3, :4)",
                                    [ts, fields[1], fields[2], fields[3]])

            connection.commit()
    except FileNotFoundError:
        print("File " + input_file + " does not exist" )
        

def check_if_table_exists(db_cursor, table_name):
    db_cursor.execute("SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = :1",[table_name.upper()])
    count = db_cursor.fetchone()
    if(count[0] == 0):
        if table_name.upper() == "METRICS":
            db_cursor.execute("CREATE TABLE METRICS (" \
            "TIME_STAMP TIMESTAMP," \
            "RAM_PCT    NUMBER(5, 2)," \
            "RAM_USED   NUMBER(7, 2)," \
            "RAM_TOTAL  NUMBER(7, 2)," \
            "DISK_PCT   NUMBER(5, 2)," \
            "CPU_PCT    NUMBER(5, 2))")
        elif table_name.upper() == "STATUS":
            db_cursor.execute("CREATE TABLE STATUS (" \
            "TIME_STAMP  TIMESTAMP," \
            "HTTP_STATUS NUMBER(5, 2)," \
            "MTLS_NO_CERT NUMBER(5, 2)," \
            "MTLS_CERT NUMBER(5, 2)) ")

with oracledb.connect(user=db_user,password=db_user_password,dsn=dsn) as connection:
    with connection.cursor() as cursor:
        check_if_table_exists(cursor,"METRICS")
        check_if_table_exists(cursor,"STATUS")
        while True:
            cursor.execute("select MAX(TIME_STAMP) from METRICS")
            result = cursor.fetchone()
            datetime_today = datetime.datetime.now()

            max_metrics_ts = result[0] if result[0] is not None else datetime.datetime.min
            date_str_today = datetime_today.strftime("%Y-%m-%d")
            datetime_yesterday = datetime_today - datetime.timedelta(days=1)
            date_str_yesterday = datetime_yesterday.strftime("%Y-%m-%d")

            health_today_path = "/logs/health-" + date_str_today + ".log"
            health_yesterday_path = "/logs/health-" + date_str_yesterday + ".log"
            service_today_path = "/logs/service-" + date_str_today + ".log"
            service_yesterday_path = "/logs/service-" + date_str_yesterday + ".log"

            insert_into_db(connection, cursor, max_metrics_ts, health_today_path)
            insert_into_db(connection, cursor, max_metrics_ts, health_yesterday_path)

            cursor.execute("select MAX(TIME_STAMP) from STATUS")
            result = cursor.fetchone()
            max_status_ts = result[0] if result[0] is not None else datetime.datetime.min
 
            insert_into_db(connection, cursor, max_status_ts, service_today_path)
            insert_into_db(connection, cursor, max_status_ts, service_yesterday_path)

            time.sleep(60)