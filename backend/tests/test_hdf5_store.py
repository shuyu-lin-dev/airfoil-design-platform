"""Tests for HDF5 artifact store (no HTTP dependency)."""

import os
import numpy as np
import h5py

from airfoil_platform.lib.ids import generate_artifact_id
from airfoil_platform.artifacts.artifact_registry import (
    artifact_dir,
    write_sidecar,
    read_sidecar,
    build_metadata,
    artifact_file_path,
)
from airfoil_platform.artifacts.hdf5_store import (
    write_hdf5_artifact,
    read_hdf5_datasets,
    get_hdf5_metadata,
)


def test_artifact_id_deterministic():
    inputs = {"cst_params": [0.1] * 12, "mach": 0.3, "angle_of_attack": 2.0}
    id1 = generate_artifact_id(inputs)
    id2 = generate_artifact_id(inputs)
    assert id1 == id2
    assert len(id1) == 12


def test_artifact_id_different_inputs():
    id1 = generate_artifact_id({"a": 1})
    id2 = generate_artifact_id({"a": 2})
    assert id1 != id2


def test_artifact_id_key_order_independent():
    id1 = generate_artifact_id({"a": 1, "b": 2})
    id2 = generate_artifact_id({"b": 2, "a": 1})
    assert id1 == id2


def test_write_and_read_hdf5():
    artifact_id = "test12345678"
    coords = np.random.rand(1000, 2).astype(np.float64)
    pressure = np.random.rand(1000).astype(np.float64)
    velocity = np.random.rand(1000).astype(np.float64)

    path = write_hdf5_artifact(artifact_id, coords, pressure, velocity)

    # Check file exists
    assert os.path.isfile(path)

    # Check datasets
    c2, p2, v2 = read_hdf5_datasets(artifact_id)
    assert c2.shape == (1000, 2)
    assert p2.shape == (1000,)
    assert v2.shape == (1000,)
    np.testing.assert_array_almost_equal(c2, coords)
    np.testing.assert_array_almost_equal(p2, pressure)
    np.testing.assert_array_almost_equal(v2, velocity)


def test_json_sidecar_written():
    artifact_id = "sidecar-test"
    coords = np.zeros((1000, 2))
    pressure = np.zeros(1000)
    velocity = np.zeros(1000)

    write_hdf5_artifact(artifact_id, coords, pressure, velocity)

    meta = get_hdf5_metadata(artifact_id)
    assert meta is not None
    assert meta["artifact_id"] == artifact_id
    assert meta["format"] == "hdf5"
    assert meta["role"] == "aerodynamic_field"
    assert meta["status"] == "ready"
    assert meta["datasets"] == {
        "coordinates": "/coordinates",
        "pressure_field": "/fields/pressure",
        "velocity_field": "/fields/velocity",
    }
    assert os.path.isfile(meta["path"])


def test_sidecar_roundtrip():
    meta = {
        "artifact_id": "abc123",
        "format": "hdf5",
        "role": "aerodynamic_field",
        "path": "/tmp/test.h5",
        "status": "ready",
        "datasets": {"x": "/x"},
    }
    write_sidecar("abc123", "aerodynamic", meta)
    read_back = read_sidecar("aerodynamic", "abc123")
    assert read_back is not None
    assert read_back["artifact_id"] == "abc123"
    assert read_back["format"] == "hdf5"


def test_read_sidecar_missing_returns_none():
    result = read_sidecar("aerodynamic", "nonexistent-id-99999")
    assert result is None


def test_hdf5_dataset_layout():
    artifact_id = "layout-test"
    coords = np.random.rand(1000, 2).astype(np.float64)
    pressure = np.random.rand(1000).astype(np.float64)
    velocity = np.random.rand(1000).astype(np.float64)

    path = write_hdf5_artifact(artifact_id, coords, pressure, velocity)

    with h5py.File(path, "r") as f:
        assert "/coordinates" in f
        assert "/fields/pressure" in f
        assert "/fields/velocity" in f
        assert f["/coordinates"].shape == (1000, 2)
        assert f["/fields/pressure"].shape == (1000,)
        assert f["/fields/velocity"].shape == (1000,)
