import datetime

class FakeDb:
    def execute(self, query: str, params=None):
        if "RAM_PCT" in query:
            return [("2026-06-24 14:00", 62.5, 5000.0), ("2026-06-24 15:00", 64.0, 5120.0)]
        elif "CPU_PCT" in query:
            return [("2026-06-24 14:00", 12.5), ("2026-06-24 15:00", 18.0)]
        elif "DISK_PCT" in query:
            return [("2026-06-24 14:00", 40.0), ("2026-06-24 15:00", 41.5)]
        elif "FETCH" in query:
            return [("2026-06-24 14:00", 200, 0, 404)]
        elif "STATUS" in query:
            return [(62, 100, 62.0)]
        elif "METRICS" in query:
            return [
                (datetime.datetime(2026, 6, 24, 14, 0, 0), 62.5, 5000.0, 8000.0, 40.0, 12.5),
                (datetime.datetime(2026, 6, 24, 14, 1, 0), 63.0, 5040.0, 8000.0, 40.1, 15.0),
            ]
        else:
            return []

    def connect(self):
        pass

    def close(self):
        pass