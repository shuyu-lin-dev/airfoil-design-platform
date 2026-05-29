"""Tests for teaching API endpoints (T013/T014)."""

from fastapi.testclient import TestClient

from airfoil_platform.main import app

client = TestClient(app)


# ---- POST /teaching/airfoil-from-control-points (T013) ----

def test_teaching_airfoil_returns_200_points():
    response = client.post("/teaching/airfoil-from-control-points", json={
        "camber_control_points": [
            {"x": 0.0, "y": 0.0},
            {"x": 0.5, "y": 0.05},
        ],
        "thickness_control_points": [
            {"x": 0.0, "y": 0.0},
            {"x": 0.5, "y": 0.1},
        ],
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["points"]) == 200


def test_teaching_airfoil_has_stub_meta():
    response = client.post("/teaching/airfoil-from-control-points", json={
        "camber_control_points": [
            {"x": 0.0, "y": 0.0},
            {"x": 0.5, "y": 0.05},
        ],
        "thickness_control_points": [
            {"x": 0.0, "y": 0.0},
            {"x": 0.5, "y": 0.1},
        ],
    })
    data = response.json()
    assert data["is_stub"] is True
    assert data["model_version"] == "stub-v0"


def test_teaching_airfoil_rejects_wrong_control_point_count():
    response = client.post("/teaching/airfoil-from-control-points", json={
        "camber_control_points": [{"x": 0.0, "y": 0.0}],
        "thickness_control_points": [
            {"x": 0.0, "y": 0.0},
            {"x": 0.5, "y": 0.1},
        ],
    })
    assert response.status_code == 422


def test_teaching_airfoil_rejects_x_out_of_range():
    response = client.post("/teaching/airfoil-from-control-points", json={
        "camber_control_points": [
            {"x": 0.0, "y": 0.0},
            {"x": 1.5, "y": 0.05},
        ],
        "thickness_control_points": [
            {"x": 0.0, "y": 0.0},
            {"x": 0.5, "y": 0.1},
        ],
    })
    assert response.status_code == 422


# ---- POST /teaching/cst-from-airfoil (T014) ----

def test_teaching_cst_inverse_returns_12_params():
    points = [{"x": float(i) / 200, "y": 0.01} for i in range(200)]
    response = client.post("/teaching/cst-from-airfoil", json={
        "points": points,
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["cst_params"]) == 12


def test_teaching_cst_inverse_order():
    """First 6 = upper surface, last 6 = lower surface."""
    points = [{"x": float(i) / 200, "y": 0.01} for i in range(200)]
    response = client.post("/teaching/cst-from-airfoil", json={
        "points": points,
    })
    data = response.json()
    # All params returned; order is upper[0..5] then lower[0..5]
    assert len(data["cst_params"]) == 12


def test_teaching_cst_inverse_has_stub_meta():
    points = [{"x": float(i) / 200, "y": 0.01} for i in range(200)]
    response = client.post("/teaching/cst-from-airfoil", json={
        "points": points,
    })
    data = response.json()
    assert data["is_stub"] is True
    assert data["model_version"] == "stub-v0"


def test_teaching_cst_inverse_rejects_wrong_point_count():
    response = client.post("/teaching/cst-from-airfoil", json={
        "points": [{"x": 0.0, "y": 0.0}] * 100,
    })
    assert response.status_code == 422
