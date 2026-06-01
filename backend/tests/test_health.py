from airfoil_platform.main import app
from tests.api_client import SyncASGIClient

client = SyncASGIClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.2.0"
