import pytest
from fastapi import FastAPI

from tests.api_client import SyncASGIClient

VALID_CST = [0.15, 0.20, 0.15, 0.10, 0.05, 0.02, 0.08, 0.10, 0.08, 0.05, 0.02, 0.01]


@pytest.fixture
def client():
    from airfoil_platform.api.optimization import router
    app = FastAPI()
    app.include_router(router)
    return SyncASGIClient(app)


class TestAeroOptimization:
    def test_returns_original_optimized_and_improvement(self, client):
        body = {
            "cst_params": VALID_CST,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
            "target_improvement_ratio": 0.1,
        }
        resp = client.post("/optimization/aerodynamic", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["original"]) == 12
        assert len(data["optimized"]) == 12
        assert data["optimized"] != data["original"]
        assert data["actual_improvement_ratio"] > 0

    def test_condition_unchanged(self, client):
        body = {
            "cst_params": VALID_CST,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
            "target_improvement_ratio": 0.1,
        }
        resp = client.post("/optimization/aerodynamic", json=body)
        assert resp.status_code == 200
        assert resp.json()["is_stub"] is True
        assert resp.json()["model_version"] == "stub-v0"

    def test_invalid_target_ratio_returns_422(self, client):
        body = {
            "cst_params": VALID_CST,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
            "target_improvement_ratio": 0.0,
        }
        resp = client.post("/optimization/aerodynamic", json=body)
        assert resp.status_code == 422


class TestStructOptimization:
    def test_returns_original_optimized_and_reduction(self, client):
        body = {
            "cst_params": VALID_CST,
            "wing_planform": {"span": 10.0, "chord": 1.0},
            "structure_design": {
                "rear_spar_web_thickness": 0.01,
                "rib_thickness": 0.004,
                "rib_spacing": 0.5,
            },
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
            "target_reduction_ratio": 0.1,
        }
        resp = client.post("/optimization/structural", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert data["actual_reduction_ratio"] >= 0
        assert data["optimized"]["rear_spar_web_thickness"] <= data["original"]["rear_spar_web_thickness"]
        assert data["is_stub"] is True

    def test_optimized_within_hard_limits(self, client):
        body = {
            "cst_params": VALID_CST,
            "wing_planform": {"span": 10.0, "chord": 1.0},
            "structure_design": {
                "rear_spar_web_thickness": 0.005,
                "rib_thickness": 0.003,
                "rib_spacing": 0.5,
            },
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
            "target_reduction_ratio": 0.1,
        }
        resp = client.post("/optimization/structural", json=body)
        data = resp.json()
        opt = data["optimized"]
        assert opt["rear_spar_web_thickness"] >= 0.002
        assert opt["rib_thickness"] >= 0.002
        assert opt["rib_spacing"] <= 1.000


class TestCoupledOptimization:
    def test_returns_coupled_improvement(self, client):
        body = {
            "cst_params": VALID_CST,
            "wing_planform": {"span": 10.0, "chord": 1.0},
            "structure_design": {
                "rear_spar_web_thickness": 0.01,
                "rib_thickness": 0.004,
                "rib_spacing": 0.5,
            },
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
            "target_improvement_ratio": 0.1,
        }
        resp = client.post("/optimization/coupled", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["original_cst"]) == 12
        assert len(data["optimized_cst"]) == 12
        assert data["actual_improvement_ratio"] != 0.0
