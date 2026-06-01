import json
import tempfile
from pathlib import Path

import h5py
import pytest
from fastapi import FastAPI

from tests.api_client import SyncASGIClient


VALID_CST = [0.15, 0.20, 0.15, 0.10, 0.05, 0.02, 0.08, 0.10, 0.08, 0.05, 0.02, 0.01]


@pytest.fixture
def client():
    import airfoil_platform.api.aerodynamics as aero_mod
    from airfoil_platform.api.aerodynamics import router

    tmpdir = tempfile.mkdtemp()
    aero_mod._artifact_root = tmpdir

    app = FastAPI()
    app.include_router(router)
    return SyncASGIClient(app), tmpdir


class TestAerodynamicPrediction:
    def test_returns_lift_drag_ratio_and_cp_and_artifact(self, client):
        sync_client, tmpdir = client
        body = {
            "cst_params": VALID_CST,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        }
        resp = sync_client.post("/aerodynamics/predict", json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert "lift_drag_ratio" in data
        assert isinstance(data["lift_drag_ratio"], float)
        assert data["lift_drag_ratio"] > 0
        assert data["is_stub"] is True
        assert data["model_version"] == "stub-v0"

    def test_cp_distribution_has_200_points(self, client):
        sync_client, _tmpdir = client
        body = {
            "cst_params": VALID_CST,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        }
        resp = sync_client.post("/aerodynamics/predict", json=body)
        data = resp.json()
        cp = data["cp_distribution"]
        assert len(cp) == 200
        for pt in cp:
            assert "x" in pt
            assert "cp" in pt
            assert isinstance(pt["x"], float)
            assert isinstance(pt["cp"], float)

    def test_field_artifact_has_valid_hdf5(self, client):
        sync_client, tmpdir = client
        body = {
            "cst_params": VALID_CST,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        }
        resp = sync_client.post("/aerodynamics/predict", json=body)
        data = resp.json()
        fa = data["field_artifact"]
        assert fa["format"] == "hdf5"
        assert fa["role"] == "aerodynamic"
        assert fa["status"] == "ready"

        # Verify HDF5 file exists with correct dataset shapes
        h5_path = Path(tmpdir) / "aerodynamic" / f"{fa['artifact_id']}.h5"
        assert h5_path.exists()
        with h5py.File(h5_path, "r") as f:
            assert f["/coordinates"].shape == (1000, 2)
            assert f["/fields/pressure"].shape == (1000,)
            assert f["/fields/velocity"].shape == (1000,)

    def test_field_artifact_sidecar_exists(self, client):
        sync_client, tmpdir = client
        body = {
            "cst_params": VALID_CST,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        }
        resp = sync_client.post("/aerodynamics/predict", json=body)
        data = resp.json()
        fa = data["field_artifact"]
        sidecar_path = Path(tmpdir) / "aerodynamic" / f"{fa['artifact_id']}.json"
        assert sidecar_path.exists()
        sidecar = json.loads(sidecar_path.read_text())
        assert sidecar["artifact_id"] == fa["artifact_id"]
        assert sidecar["format"] == "hdf5"
        assert sidecar["role"] == "aerodynamic"
        assert sidecar["status"] == "ready"

    def test_artifact_id_deterministic(self, client):
        sync_client, _tmpdir = client
        body = {
            "cst_params": VALID_CST,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        }
        resp1 = sync_client.post("/aerodynamics/predict", json=body)
        resp2 = sync_client.post("/aerodynamics/predict", json=body)
        id1 = resp1.json()["field_artifact"]["artifact_id"]
        id2 = resp2.json()["field_artifact"]["artifact_id"]
        assert id1 == id2


class TestAerodynamicValidation:
    @pytest.mark.parametrize("bad_cst", [
        [0.1] * 11,
        [0.1] * 13,
        [],
        [0.1] * 20,
    ])
    def test_wrong_cst_count_returns_422(self, bad_cst):
        from airfoil_platform.api.aerodynamics import router
        import airfoil_platform.api.aerodynamics as aero_mod

        aero_mod._artifact_root = tempfile.mkdtemp()
        app = FastAPI()
        app.include_router(router)
        client = SyncASGIClient(app)
        body = {
            "cst_params": bad_cst,
            "condition": {"mach": 0.3, "angle_of_attack": 2.0},
        }
        resp = client.post("/aerodynamics/predict", json=body)
        assert resp.status_code == 422

    def test_missing_condition_returns_422(self):
        from airfoil_platform.api.aerodynamics import router
        import airfoil_platform.api.aerodynamics as aero_mod

        aero_mod._artifact_root = tempfile.mkdtemp()
        app = FastAPI()
        app.include_router(router)
        client = SyncASGIClient(app)
        resp = client.post("/aerodynamics/predict", json={"cst_params": VALID_CST})
        assert resp.status_code == 422
