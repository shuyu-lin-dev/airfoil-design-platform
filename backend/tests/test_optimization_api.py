"""Tests for optimization API — aerodynamic (T010) and structural (T011)."""

from fastapi.testclient import TestClient

from airfoil_platform.main import app

client = TestClient(app)

VALID_CST = [0.1, 0.15, 0.12, 0.1, 0.08, 0.05, -0.1, -0.12, -0.1, -0.08, -0.05, -0.02]


# ---- POST /optimization/aerodynamic (T010) ----

def test_aero_opt_returns_original_and_optimized():
    response = client.post("/optimization/aerodynamic", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "target_improvement_ratio": 0.1,
    })
    assert response.status_code == 200
    data = response.json()
    assert "original" in data
    assert "optimized" in data
    assert "actual_improvement_ratio" in data


def test_aero_opt_only_changes_cst_params():
    response = client.post("/optimization/aerodynamic", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "target_improvement_ratio": 0.1,
    })
    data = response.json()
    assert data["original"]["condition"] == data["optimized"]["condition"]
    assert data["original"]["cst_params"] != data["optimized"]["cst_params"]


def test_aero_opt_has_stub_meta():
    response = client.post("/optimization/aerodynamic", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "target_improvement_ratio": 0.1,
    })
    data = response.json()
    assert data["is_stub"] is True
    assert data["model_version"] == "stub-v0"


def test_aero_opt_rejects_invalid_ratio():
    response = client.post("/optimization/aerodynamic", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "target_improvement_ratio": 1.5,
    })
    assert response.status_code == 422


# ---- POST /optimization/structural (T011) ----

def test_struct_opt_returns_original_and_optimized():
    response = client.post("/optimization/structural", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "target_reduction_ratio": 0.1,
    })
    assert response.status_code == 200
    data = response.json()
    assert "original" in data
    assert "optimized" in data
    assert "actual_reduction_ratio" in data


def test_struct_opt_only_changes_structure_design():
    response = client.post("/optimization/structural", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "target_reduction_ratio": 0.1,
    })
    data = response.json()
    assert data["original"]["cst_params"] == data["optimized"]["cst_params"]
    assert data["original"]["condition"] == data["optimized"]["condition"]
    assert data["original"]["structure_design"] != data["optimized"]["structure_design"]


def test_struct_opt_optimized_within_range():
    response = client.post("/optimization/structural", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "target_reduction_ratio": 0.1,
    })
    data = response.json()
    opt_sd = data["optimized"]["structure_design"]
    assert 0.002 <= opt_sd["rear_spar_web_thickness"] <= 0.020
    assert 0.002 <= opt_sd["rib_thickness"] <= 0.005
    assert 0.300 <= opt_sd["rib_spacing"] <= 1.000


def test_struct_opt_weight_decreased():
    response = client.post("/optimization/structural", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "target_reduction_ratio": 0.1,
    })
    data = response.json()
    assert data["optimized"]["weight"] < data["original"]["weight"]
