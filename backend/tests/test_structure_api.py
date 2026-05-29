"""Tests for structure prediction API."""

from fastapi.testclient import TestClient

from airfoil_platform.main import app

client = TestClient(app)

VALID_CST = [0.1, 0.15, 0.12, 0.1, 0.08, 0.05, -0.1, -0.12, -0.1, -0.08, -0.05, -0.02]


def test_structure_predict_returns_max_stress_and_weight():
    response = client.post("/structure/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    assert response.status_code == 200
    data = response.json()
    assert "max_stress" in data
    assert "weight" in data
    assert data["max_stress"] > 0
    assert data["weight"] > 0


def test_structure_predict_has_stub_meta():
    response = client.post("/structure/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    data = response.json()
    assert data["is_stub"] is True
    assert data["model_version"] == "stub-v0"


def test_structure_predict_no_mass_field():
    """API must not expose mass field."""
    response = client.post("/structure/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    data = response.json()
    assert "mass" not in data


def test_structure_predict_with_custom_materials():
    response = client.post("/structure/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "material_properties": {
            "skin": {"elastic_modulus": 70e9, "material_density": 2700},
            "internal_structure": {"elastic_modulus": 200e9, "material_density": 7850},
        },
    })
    assert response.status_code == 200
    data = response.json()
    assert data["weight"] > 0


def test_structure_predict_weight_changes_with_params():
    """Heavier structure should have higher weight."""
    resp1 = client.post("/structure/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    resp2 = client.post("/structure/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.015,  # thicker
            "rib_thickness": 0.004,  # thicker
            "rib_spacing": 0.3,  # more ribs
        },
    })
    w1 = resp1.json()["weight"]
    w2 = resp2.json()["weight"]
    assert w2 > w1


def test_structure_predict_defaults_material():
    response = client.post("/structure/predict", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    assert response.status_code == 200


def test_structure_predict_rejects_invalid_cst():
    response = client.post("/structure/predict", json={
        "cst_params": [0.1] * 11,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    assert response.status_code == 422
