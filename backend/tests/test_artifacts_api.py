import json
import tempfile
from pathlib import Path

import numpy as np
import pytest
from fastapi import FastAPI

from tests.api_client import SyncASGIClient


@pytest.fixture
def client():
    """Create a FastAPI app with artifacts router and temp artifact store."""
    import airfoil_platform.api.artifacts as artifacts_mod
    from airfoil_platform.api.artifacts import router

    tmpdir = tempfile.mkdtemp()
    artifacts_mod._artifact_root = tmpdir

    app = FastAPI()
    app.include_router(router)
    return SyncASGIClient(app), tmpdir


def _create_test_artifact(artifact_root, artifact_id):
    """Write a small HDF5 artifact + sidecar for API testing."""
    from airfoil_platform.artifacts.hdf5_store import write_hdf5_artifact

    coords = np.array([[0.0, 0.0], [1.0, 0.1]], dtype=np.float64)
    pressure = np.array([101325.0, 101000.0], dtype=np.float64)
    velocity = np.array([50.0, 55.0], dtype=np.float64)

    return write_hdf5_artifact(
        artifact_id=artifact_id,
        coordinates=coords,
        pressure=pressure,
        velocity=velocity,
        artifact_root=artifact_root,
    )


class TestArtifactMetadata:
    def test_returns_sidecar_content(self, client):
        sync_client, tmpdir = client
        artifact_id = "meta000000001"
        sidecar = _create_test_artifact(tmpdir, artifact_id)

        resp = sync_client.get(f"/artifacts/{artifact_id}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["artifact_id"] == artifact_id
        assert body["format"] == "hdf5"
        assert body["role"] == "aerodynamic"
        assert body["status"] == "ready"
        assert "/coordinates" in body["datasets"]
        assert "/fields/pressure" in body["datasets"]
        assert "/fields/velocity" in body["datasets"]

    def test_nonexistent_returns_404(self, client):
        sync_client, _tmpdir = client
        resp = sync_client.get("/artifacts/doesnotexist")
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"].lower()

    def test_metadata_reads_from_disk_not_registry(self, client):
        """Metadata must be served from JSON sidecar, not from in-memory registry."""
        sync_client, tmpdir = client
        artifact_id = "disk000000001"
        _sidecar = _create_test_artifact(tmpdir, artifact_id)

        # First request should succeed (reads from disk)
        resp = sync_client.get(f"/artifacts/{artifact_id}")
        assert resp.status_code == 200

        # Modify the sidecar on disk
        sidecar_path = Path(tmpdir) / "aerodynamic" / f"{artifact_id}.json"
        modified = json.loads(sidecar_path.read_text())
        modified["status"] = "pending"
        sidecar_path.write_text(json.dumps(modified))

        # Second request should reflect the disk change (not cached value)
        resp2 = sync_client.get(f"/artifacts/{artifact_id}")
        assert resp2.status_code == 200
        assert resp2.json()["status"] == "pending"


class TestArtifactDownload:
    def test_download_returns_hdf5_file(self, client):
        sync_client, tmpdir = client
        artifact_id = "down000000001"
        sidecar = _create_test_artifact(tmpdir, artifact_id)

        resp = sync_client.get(f"/artifacts/{artifact_id}/download")
        assert resp.status_code == 200

        # Write response bytes to temp file and verify with h5py
        import h5py
        tmp_file = Path(tmpdir) / "downloaded.h5"
        tmp_file.write_bytes(resp.body)
        with h5py.File(tmp_file, "r") as f:
            assert f["/coordinates"].shape == (2, 2)
            assert f["/fields/pressure"].shape == (2,)
            assert f["/fields/velocity"].shape == (2,)

    def test_download_nonexistent_returns_404(self, client):
        sync_client, _tmpdir = client
        resp = sync_client.get("/artifacts/nonexistent/download")
        assert resp.status_code == 404
