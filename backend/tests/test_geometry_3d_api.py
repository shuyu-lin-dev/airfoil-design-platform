"""Tests for geometry API — 3D wing endpoints."""

import os
from fastapi.testclient import TestClient

from airfoil_platform.main import app
from airfoil_platform.core.geometry import read_step_components, compute_rib_positions

client = TestClient(app)

VALID_CST = [0.1, 0.15, 0.12, 0.1, 0.08, 0.05, -0.1, -0.12, -0.1, -0.08, -0.05, -0.02]


def test_wing_3d_returns_geometry_artifact():
    response = client.post("/geometry/wing-3d", json={
        "cst_params": VALID_CST,
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    assert response.status_code == 200
    data = response.json()
    ga = data["geometry_artifact"]
    assert ga["format"] == "step"
    assert ga["role"] == "structural_step"
    assert ga["status"] == "ready"
    assert len(ga["artifact_id"]) == 12
    assert ga["components"] == ["skin", "front_spar", "rear_spar", "ribs"]


def test_wing_3d_has_stub_meta():
    response = client.post("/geometry/wing-3d", json={
        "cst_params": VALID_CST,
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


def test_wing_3d_step_file_exists_and_valid():
    response = client.post("/geometry/wing-3d", json={
        "cst_params": VALID_CST,
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    data = response.json()
    step_path = data["geometry_artifact"]["path"]
    assert os.path.isfile(step_path)
    sidecar = step_path.replace(".step", ".json")
    assert os.path.isfile(sidecar)


def test_wing_3d_step_readable_and_bbox_correct():
    response = client.post("/geometry/wing-3d", json={
        "cst_params": VALID_CST,
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    data = response.json()
    step_path = data["geometry_artifact"]["path"]
    shapes, bbox = read_step_components(step_path)
    assert len(shapes) > 0
    assert bbox is not None
    assert 0 <= bbox["xmin"] <= 0.01
    assert 0.99 <= bbox["xmax"] <= 1.01 + 0.02
    assert -0.01 <= bbox["zmin"] <= 0.01
    assert 4.9 <= bbox["zmax"] <= 5.1
    assert bbox["ymin"] < 0 < bbox["ymax"]


def test_wing_3d_rib_count_matches_rib_spacing():
    response = client.post("/geometry/wing-3d", json={
        "cst_params": VALID_CST,
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    assert response.status_code == 200
    semi_span = 5.0
    rib_spacing = 0.5
    expected_rib_count = int(semi_span / rib_spacing) + 1
    positions = compute_rib_positions(semi_span, rib_spacing)
    assert len(positions) == expected_rib_count


def test_wing_3d_uses_default_wing_planform():
    response = client.post("/geometry/wing-3d", json={
        "cst_params": VALID_CST,
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    assert response.status_code == 200
    data = response.json()
    assert data["geometry_artifact"]["status"] == "ready"


def test_wing_3d_rejects_invalid_cst():
    response = client.post("/geometry/wing-3d", json={
        "cst_params": [0.1] * 11,
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    assert response.status_code == 422


def test_wing_3d_rejects_invalid_structure_design():
    response = client.post("/geometry/wing-3d", json={
        "cst_params": VALID_CST,
        "structure_design": {
            "rear_spar_web_thickness": 0.05,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    assert response.status_code == 422


def test_wing_3d_returns_artifact_not_point_cloud():
    """Wing-3d must NOT return 1000 3D point cloud."""
    response = client.post("/geometry/wing-3d", json={
        "cst_params": VALID_CST,
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    })
    data = response.json()
    assert "points" not in data
    assert "point_cloud" not in data
    assert "geometry_artifact" in data
