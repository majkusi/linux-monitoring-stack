import oracledb

class Connect:
    def __init__(self, db_user: str, db_user_password: str, db_dsn: str):
        self.db_user = db_user
        self.db_user_password = db_user_password
        self.db_dsn = db_dsn
        self.pool: oracledb.ConnectionPool | None = None

    def connect(self):
        self.pool = oracledb.create_pool(
            user=self.db_user,
            password=self.db_user_password,
            dsn=self.db_dsn,
        )

    def execute(self, query: str, params=None):
        if self.pool is None:
            raise RuntimeError("Pool not initialized — call connect() first")
        with self.pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params or [])
                return cursor.fetchall()

    def close(self):
        if self.pool is not None:
            self.pool.close()