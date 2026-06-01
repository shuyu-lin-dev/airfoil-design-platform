import pytest
from fastapi import FastAPI

from tests.api_client import SyncASGIClient


@pytest.fixture
def client():
    from airfoil_platform.api.teaching import router
    app = FastAPI()
    app.include_router(router)
    return SyncASGIClient(app)


class TestAirfoilFromControlPoints:
    def test_returns_200_points(self, client):
        body = {
            "camber_control_points": [{"x": 0.0, "y": 0.0}, {"x": 1.0, "y": 0.02}],
            "thickness_control_points": [{"x": 0.0, "y": 0.0}, {"x": 0.4, "y": 0.08}],
        }
        resp = client.post("/teaching/airfoil-from-control-points", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["points"]) == 200
        assert data["is_stub"] is True
        assert data["model_version"] == "stub-v0"

    def test_upper_and_lower_different_for_cambered(self, client):
        body = {
            "camber_control_points": [{"x": 0.0, "y": 0.0}, {"x": 1.0, "y": 0.05}],
            "thickness_control_points": [{"x": 0.0, "y": 0.0}, {"x": 0.4, "y": 0.08}],
        }
        resp = client.post("/teaching/airfoil-from-control-points", json=body)
        points = resp.json()["points"]
        # For a cambered airfoil, upper and lower mid-chord y values should differ
        assert points[50]["y"] != points[150]["y"]


class TestCstFromAirfoil:
    def test_returns_12_cst_params(self, client):
        points = [{"x": i / 199.0, "y": 0.01} for i in range(100)] + [
            {"x": i / 199.0, "y": -0.01} for i in range(100)
        ]
        resp = client.post("/teaching/cst-from-airfoil", json={"points": points})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["cst_params"]) == 12
        assert data["is_stub"] is True
