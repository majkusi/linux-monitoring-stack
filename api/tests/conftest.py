import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

os.environ["APP_USER"] = "test_user"
os.environ["APP_USER_PASSWORD"] = "test_pass"
os.environ["DB_SERVICE"] = "test_dsn"
os.environ["DB_HOST"] = "test_host"
os.environ["DB_PORT"] = "test_port"

from misc.fakeDb import FakeDb
from fastapi.testclient import TestClient
from main import app
from main import get_db
import pytest

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: FakeDb()
    return TestClient(app)