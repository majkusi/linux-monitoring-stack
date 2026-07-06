import datetime
class FakeDb:
    def execute(self, query: str, params=None):
        if "RAM_PCT" in query:
            return [("2026-06-24 14:00", 62.5, 5000.0),("2026-06-24 15:00", 64.0, 5120.0)]
        if "CPU_PCT" in query:
            return [("2026-06-24 14:00", 12.5),("2026-06-24 15:00", 18.0)]
        if "DISK_PCT" in query:
            return [("2026-06-24 14:00", 40.0),("2026-06-24 15:00", 41.5)]
        if "HTTP" in query:
            return [("2026-06-24 14:00",200,000,404)]
        else:
            return[(datetime.datetime(2026, 6, 24, 14, 0, 0), 62.5, 5000.0, 8000.0, 40.0, 12.5),(datetime.datetime(2026, 6, 24, 14, 1, 0), 63.0, 5040.0, 8000.0, 40.1, 15.0)]