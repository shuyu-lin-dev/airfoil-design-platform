import json
import math
import tempfile
from pathlib import Path

import cadquery as cq
import pytest
from fastapi import FastAPI

from tests.api_client import SyncASGIClient


@pytest.fixture
def client_3d():
    import airfoil_platform.api.geometry as geo_mod
    from airfoil_platform.api.geometry import router

    tmpdir = tempfile.mkdtemp()
    geo_mod._artifact_root = tmpdir

    app = FastAPI()
    app.include_router(router)
    return SyncASGIClient(app), tmpdir


VALID_CST = [0.15, 0.20, 0.15, 0.10, 0.05, 0.02, 0.08, 0.10, 0.08, 0.05, 0.02, 0.01]


def _make_body():
    return {
        "cst_params": VALID_CST,
        "wing_planform": {"span": 10.0, "chord": 1.0},
        "structure_design": {
            "rear_spar_web_thickness": 0.005,
            "rib_thickness": 0.003,
            "rib_spacing": 0.5,
        },
    }


class TestWing3D:
    def test_returns_geometry_artifact(self, client_3d):
        sync, _tmpdir = client_3d
        resp = sync.post("/geometry/wing-3d", json=_make_body())
        assert resp.status_code == 200
        data = resp.json()
        ga = data["geometry_artifact"]
        assert ga["format"] == "step"
        assert ga["role"] == "structural_step"
        assert ga["status"] == "ready"
        assert data["is_stub"] is True
        assert data["model_version"] == "stub-v0"

    def test_step_file_exists_and_non_empty(self, client_3d):
        sync, tmpdir = client_3d
        resp = sync.post("/geometry/wing-3d", json=_make_body())
        ga = resp.json()["geometry_artifact"]
        step_path = Path(tmpdir) / "geometry" / f"{ga['artifact_id']}.step"
        assert step_path.exists()
        assert step_path.stat().st_size > 0

    def test_step_can_be_reimported_with_cadquery(self, client_3d):
        sync, tmpdir = client_3d
        resp = sync.post("/geometry/wing-3d", json=_make_body())
        ga = resp.json()["geometry_artifact"]
        step_path = str(Path(tmpdir) / "geometry" / f"{ga['artifact_id']}.step")
        imported = cq.importers.importStep(step_path)
        assert imported is not None
        solids = imported.findSolid()
        assert solids is not None

    def test_components_cover_skin_spars_ribs(self, client_3d):
        sync, _tmpdir = client_3d
        resp = sync.post("/geometry/wing-3d", json=_make_body())
        components = resp.json()["geometry_artifact"]["components"]
        assert "skin" in components
        assert "front_spar" in components
        assert "rear_spar" in components
        rib_names = [c for c in components if c.startswith("rib_")]
        assert len(rib_names) > 0

    def test_bounding_box_matches_chord_and_half_span(self, client_3d):
        sync, tmpdir = client_3d
        resp = sync.post("/geometry/wing-3d", json=_make_body())
        ga = resp.json()["geometry_artifact"]
        step_path = str(Path(tmpdir) / "geometry" / f"{ga['artifact_id']}.step")
        imported = cq.importers.importStep(step_path)
        bb = imported.findSolid().BoundingBox()
        assert abs(bb.xmax - 1.0) < 0.3
        assert abs(bb.zmax - 5.0) < 0.5
        assert abs(bb.zmin) < 0.1

    def test_rib_count_matches_spacing(self, client_3d):
        sync, _tmpdir = client_3d
        body = _make_body()
        body["structure_design"]["rib_spacing"] = 0.5
        resp = sync.post("/geometry/wing-3d", json=body)
        components = resp.json()["geometry_artifact"]["components"]
        rib_names = [c for c in components if c.startswith("rib_")]
        assert len(rib_names) == 11

    def test_invalid_structure_returns_422(self, client_3d):
        sync, _tmpdir = client_3d
        body = _make_body()
        body["structure_design"]["rib_spacing"] = 0.1
        resp = sync.post("/geometry/wing-3d", json=body)
        assert resp.status_code == 422
