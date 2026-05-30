"""Tests for optimization API — coupled optimization (T012)."""

from fastapi.testclient import TestClient

from airfoil_platform.main import app

client = TestClient(app)

VALID_CST = [0.1, 0.15, 0.12, 0.1, 0.08, 0.05, -0.1, -0.12, -0.1, -0.08, -0.05, -0.02]


def test_coupled_opt_returns_fitness():
    response = client.post("/optimization/coupled", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "target_improvement_ratio": 0.1,
    })
    assert response.status_code == 200
    data = response.json()
    assert "fitness" in data["original"]
    assert "fitness" in data["optimized"]
    assert "weight" in data["original"]
    assert "lift_drag_ratio" in data["original"]


def test_coupled_opt_fitness_increases():
    response = client.post("/optimization/coupled", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "target_improvement_ratio": 0.1,
    })
    data = response.json()
    assert data["optimized"]["fitness"] > data["original"]["fitness"]


def test_coupled_opt_fitness_formula():
    response = client.post("/optimization/coupled", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "target_improvement_ratio": 0.1,
    })
    data = response.json()
    orig_f = data["original"]["lift_drag_ratio"] / data["original"]["weight"]
    opt_f = data["optimized"]["lift_drag_ratio"] / data["optimized"]["weight"]
    assert abs(data["original"]["fitness"] - orig_f) < 1e-6
    assert abs(data["optimized"]["fitness"] - opt_f) < 1e-6


def test_coupled_opt_does_not_change_condition():
    response = client.post("/optimization/coupled", json={
        "cst_params": VALID_CST,
        "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        "wing_planform": {},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
        "target_improvement_ratio": 0.1,
    })
    data = response.json()
    assert data["original"]["condition"] == data["optimized"]["condition"]
    assert data["original"]["wing_planform"] == data["optimized"]["wing_planform"]
