"""Tests for aerodynamic prediction API."""

import os
from fastapi.testclient import TestClient

from airfoil_platform.main import app

client = TestClient(app)

VALID_CST = [0.1, 0.15, 0.12, 0.1, 0.08, 0.05, -0.1, -0.12, -0.1, -0.08, -0.05, -0.02]


def test_aero_predict_returns_lift_drag_ratio():
    response = client.post("/aerodynamics/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
    })
    assert response.status_code == 200
    data = response.json()
    assert "lift_drag_ratio" in data
    assert isinstance(data["lift_drag_ratio"], float)


def test_aero_predict_returns_200_cp_points():
    response = client.post("/aerodynamics/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
    })
    data = response.json()
    assert len(data["cp_distribution"]) == 200
    cp0 = data["cp_distribution"][0]
    assert "x" in cp0 and "y" in cp0 and "cp" in cp0


def test_aero_predict_returns_field_artifact():
    response = client.post("/aerodynamics/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
    })
    data = response.json()
    fa = data["field_artifact"]
    assert fa["format"] == "hdf5"
    assert fa["role"] == "aerodynamic_field"
    assert fa["status"] == "ready"
    assert len(fa["artifact_id"]) == 12
    assert "datasets" in fa


def test_aero_predict_hdf5_file_exists():
    response = client.post("/aerodynamics/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.5, "angle_of_attack": 1.0},
    })
    data = response.json()
    artifact_path = data["field_artifact"]["path"]
    assert os.path.isfile(artifact_path)
    # JSON sidecar exists
    sidecar = artifact_path.replace(".h5", ".json")
    assert os.path.isfile(sidecar)


def test_aero_predict_has_stub_meta():
    response = client.post("/aerodynamics/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
    })
    data = response.json()
    assert data["is_stub"] is True
    assert data["model_version"] == "stub-v0"


def test_aero_predict_pressure_velocity_not_in_json():
    """Pressure and velocity fields must NOT be in JSON response."""
    response = client.post("/aerodynamics/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
    })
    data = response.json()
    assert "pressure" not in data
    assert "velocity" not in data
    assert "pressure_field" not in data
    assert "velocity_field" not in data


def test_aero_predict_rejects_invalid_cst():
    response = client.post("/aerodynamics/predict", json={
        "cst_params": [0.1] * 11,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
    })
    assert response.status_code == 422


def test_same_input_produces_same_artifact_id():
    resp1 = client.post("/aerodynamics/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.4, "angle_of_attack": 3.0},
    })
    resp2 = client.post("/aerodynamics/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.4, "angle_of_attack": 3.0},
    })
    assert resp1.json()["field_artifact"]["artifact_id"] == \
           resp2.json()["field_artifact"]["artifact_id"]
