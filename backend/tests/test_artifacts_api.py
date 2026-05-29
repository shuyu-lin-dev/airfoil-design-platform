"""Tests for artifact query and download API."""

import numpy as np
from fastapi.testclient import TestClient

from airfoil_platform.main import app
from airfoil_platform.artifacts.hdf5_store import write_hdf5_artifact

client = TestClient(app)


def _create_test_artifact(artifact_id: str):
    coords = np.zeros((1000, 2))
    pressure = np.zeros(1000)
    velocity = np.zeros(1000)
    write_hdf5_artifact(artifact_id, coords, pressure, velocity)


def test_get_artifact_meta_from_sidecar():
    _create_test_artifact("meta-query-1")
    response = client.get("/artifacts/meta-query-1")
    assert response.status_code == 200
    data = response.json()
    assert data["artifact_id"] == "meta-query-1"
    assert data["format"] == "hdf5"
    assert data["role"] == "aerodynamic_field"
    assert data["status"] == "ready"
    assert "datasets" in data


def test_get_artifact_meta_not_found():
    response = client.get("/artifacts/nonexistent-xyz")
    assert response.status_code == 404


def test_download_artifact_file():
    _create_test_artifact("download-test")
    response = client.get("/artifacts/download-test/download")
    assert response.status_code == 200
    assert "hdf" in response.headers["content-type"]
    # Content should be non-empty binary
    assert len(response.content) > 0


def test_download_artifact_not_found():
    response = client.get("/artifacts/nonexistent-xyz/download")
    assert response.status_code == 404


def test_meta_and_download_are_separate():
    """Meta query returns JSON, download returns file."""
    _create_test_artifact("sep-test")
    meta_resp = client.get("/artifacts/sep-test")
    assert meta_resp.status_code == 200
    assert meta_resp.headers["content-type"] == "application/json"

    dl_resp = client.get("/artifacts/sep-test/download")
    assert dl_resp.status_code == 200
    assert "application/x-hdf" in dl_resp.headers["content-type"]
