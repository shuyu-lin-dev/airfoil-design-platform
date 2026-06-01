import pytest
from fastapi import FastAPI

from tests.api_client import SyncASGIClient

VALID_CST = [0.15, 0.20, 0.15, 0.10, 0.05, 0.02, 0.08, 0.10, 0.08, 0.05, 0.02, 0.01]


@pytest.fixture
def client():
    from airfoil_platform.api.structure import router
    app = FastAPI()
    app.include_router(router)
    return SyncASGIClient(app)


def _make_body():
    return {
        "cst_params": VALID_CST,
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
    }


class TestStructurePrediction:
    def test_returns_max_stress_and_weight(self, client):
        resp = client.post("/structure/predict", json=_make_body())
        assert resp.status_code == 200
        data = resp.json()
        assert "max_stress" in data
        assert "weight" in data
        assert isinstance(data["max_stress"], (int, float))
        assert isinstance(data["weight"], (int, float))
        assert data["max_stress"] > 0
        assert data["weight"] > 0
        assert data["is_stub"] is True
        assert data["model_version"] == "stub-v0"

    def test_default_materials_used_when_omitted(self, client):
        resp = client.post("/structure/predict", json=_make_body())
        assert resp.status_code == 200

    def test_custom_materials_accepted(self, client):
        body = _make_body()
        body["material_properties"] = {
            "skin": {"elastic_modulus": 70e9, "material_density": 2700},
            "internal_structure": {"elastic_modulus": 200e9, "material_density": 7850},
        }
        resp = client.post("/structure/predict", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert data["max_stress"] > 0
        assert data["weight"] > 0

    def test_missing_structure_design_returns_422(self, client):
        body = {
            "cst_params": VALID_CST,
            "wing_planform": {"span": 10.0, "chord": 1.0},
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        }
        resp = client.post("/structure/predict", json=body)
        assert resp.status_code == 422
