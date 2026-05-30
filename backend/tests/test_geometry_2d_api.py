"""Tests for geometry API — 2D airfoil endpoints."""

from fastapi.testclient import TestClient

from airfoil_platform.main import app

client = TestClient(app)


def test_airfoil_2d_returns_200_points():
    response = client.post("/geometry/airfoil-2d", json={
        "cst_params": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1],
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["points"]) == 200


def test_airfoil_2d_first_100_upper_last_100_lower():
    response = client.post("/geometry/airfoil-2d", json={
        "cst_params": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1],
    })
    data = response.json()
    upper = data["points"][:100]
    lower = data["points"][100:]
    for p in upper:
        assert "x" in p and "y" in p
    for p in lower:
        assert "x" in p and "y" in p
    avg_upper_y = sum(p["y"] for p in upper) / 100
    avg_lower_y = sum(p["y"] for p in lower) / 100
    assert avg_upper_y > avg_lower_y


def test_airfoil_2d_has_stub_meta():
    response = client.post("/geometry/airfoil-2d", json={
        "cst_params": [0.1] * 12,
    })
    data = response.json()
    assert data["is_stub"] is True
    assert data["model_version"] == "stub-v0"


def test_airfoil_2d_rejects_wrong_cst_count():
    response = client.post("/geometry/airfoil-2d", json={
        "cst_params": [0.1] * 11,
    })
    assert response.status_code == 422


def test_airfoil_2d_rejects_13_cst_params():
    response = client.post("/geometry/airfoil-2d", json={
        "cst_params": [0.1] * 13,
    })
    assert response.status_code == 422


def test_airfoil_2d_each_point_is_2d():
    response = client.post("/geometry/airfoil-2d", json={
        "cst_params": [0.2] * 12,
    })
    data = response.json()
    for p in data["points"]:
        assert isinstance(p["x"], (int, float))
        assert isinstance(p["y"], (int, float))
