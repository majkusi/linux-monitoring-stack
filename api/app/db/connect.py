import oracledb

class Connect:
    def __init__(self, user: str, password: str, dsn: str):
        self.user = user
        self.password = password
        self.dsn = dsn
        self.pool: oracledb.ConnectionPool | None = None

    def connect(self):
        self.pool = oracledb.create_pool(
            user=self.user,
            password=self.password,
            dsn=self.dsn,
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