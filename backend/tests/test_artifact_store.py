import json
import tempfile
from pathlib import Path

import h5py
import numpy as np

from airfoil_platform.artifacts import (
    ArtifactRegistry,
    ArtifactMetadata,
    generate_artifact_id,
    write_hdf5_artifact,
)


class TestArtifactIdGeneration:

    def test_deterministic(self):
        id1 = generate_artifact_id({"a": 1, "b": 2})
        id2 = generate_artifact_id({"a": 1, "b": 2})
        assert id1 == id2

    def test_key_order_independent(self):
        id1 = generate_artifact_id({"a": 1, "b": 2})
        id2 = generate_artifact_id({"b": 2, "a": 1})
        assert id1 == id2

    def test_different_inputs_different_ids(self):
        id1 = generate_artifact_id({"a": 1})
        id2 = generate_artifact_id({"a": 2})
        assert id1 != id2

    def test_output_is_12_hex_chars(self):
        aid = generate_artifact_id({"test": 1})
        assert len(aid) == 12
        assert all(c in "0123456789abcdef" for c in aid)


class TestHDF5Store:

    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.coords = np.random.RandomState(42).rand(1000, 2).astype(np.float64)
        self.pressure = np.random.RandomState(43).rand(1000).astype(np.float64)
        self.velocity = np.random.RandomState(44).rand(1000).astype(np.float64)

    def teardown_method(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_write_hdf5_and_sidecar(self):
        artifact_id = "test12345678"
        meta = write_hdf5_artifact(
            artifact_id=artifact_id,
            coordinates=self.coords,
            pressure=self.pressure,
            velocity=self.velocity,
            artifact_root=self.tmpdir,
        )

        # JSON sidecar exists and has correct fields
        sidecar_path = Path(self.tmpdir) / "aerodynamic" / f"{artifact_id}.json"
        assert sidecar_path.exists()
        sidecar = json.loads(sidecar_path.read_text())
        assert sidecar["artifact_id"] == artifact_id
        assert sidecar["format"] == "hdf5"
        assert sidecar["role"] == "aerodynamic"
        assert sidecar["status"] == "ready"
        assert "/coordinates" in sidecar["datasets"]
        assert "/fields/pressure" in sidecar["datasets"]
        assert "/fields/velocity" in sidecar["datasets"]

        # HDF5 file exists with correct datasets
        h5_path = Path(self.tmpdir) / "aerodynamic" / f"{artifact_id}.h5"
        assert h5_path.exists()
        with h5py.File(h5_path, "r") as f:
            assert f["/coordinates"].shape == (1000, 2)
            assert f["/fields/pressure"].shape == (1000,)
            assert f["/fields/velocity"].shape == (1000,)
            np.testing.assert_array_almost_equal(f["/coordinates"][:], self.coords)
            np.testing.assert_array_almost_equal(f["/fields/pressure"][:], self.pressure)
            np.testing.assert_array_almost_equal(f["/fields/velocity"][:], self.velocity)

        # Returned metadata matches
        assert meta["artifact_id"] == artifact_id
        assert meta["format"] == "hdf5"

    def test_creates_directories_if_missing(self):
        deep_root = Path(self.tmpdir) / "nested" / "deep"
        artifact_id = "deeptest0000"
        meta = write_hdf5_artifact(
            artifact_id=artifact_id,
            coordinates=self.coords,
            pressure=self.pressure,
            velocity=self.velocity,
            artifact_root=str(deep_root),
        )
        h5_path = deep_root / "aerodynamic" / f"{artifact_id}.h5"
        assert h5_path.exists()
        assert meta["status"] == "ready"


class TestArtifactRegistry:

    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.coords = np.random.RandomState(42).rand(1000, 2).astype(np.float64)
        self.pressure = np.random.RandomState(43).rand(1000).astype(np.float64)
        self.velocity = np.random.RandomState(44).rand(1000).astype(np.float64)

    def teardown_method(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_register_and_get_from_cache(self):
        registry = ArtifactRegistry(self.tmpdir)
        meta = ArtifactMetadata(
            artifact_id="abc123",
            format="hdf5",
            role="aerodynamic",
            path="aerodynamic/abc123.h5",
            status="ready",
            datasets=["/coordinates", "/fields/pressure", "/fields/velocity"],
        )
        registry.register(meta)
        retrieved = registry.get("abc123")
        assert retrieved is not None
        assert retrieved.artifact_id == "abc123"
        assert retrieved.format == "hdf5"
        assert retrieved.role == "aerodynamic"

    def test_get_from_sidecar(self):
        artifact_id = "sidecar12345"
        write_hdf5_artifact(
            artifact_id=artifact_id,
            coordinates=self.coords,
            pressure=self.pressure,
            velocity=self.velocity,
            artifact_root=self.tmpdir,
        )

        registry = ArtifactRegistry(self.tmpdir)
        retrieved = registry.get(artifact_id)
        assert retrieved is not None
        assert retrieved.artifact_id == artifact_id
        assert retrieved.format == "hdf5"
        assert retrieved.role == "aerodynamic"
        assert retrieved.status == "ready"
        assert "/coordinates" in retrieved.datasets

    def test_get_nonexistent_returns_none(self):
        registry = ArtifactRegistry(self.tmpdir)
        assert registry.get("nonexistent") is None

    def test_cache_avoids_disk_read(self):
        artifact_id = "cachetest0001"
        write_hdf5_artifact(
            artifact_id=artifact_id,
            coordinates=self.coords,
            pressure=self.pressure,
            velocity=self.velocity,
            artifact_root=self.tmpdir,
        )

        registry = ArtifactRegistry(self.tmpdir)
        first = registry.get(artifact_id)

        # Tamper with sidecar to verify cache is used
        sidecar_path = Path(self.tmpdir) / "aerodynamic" / f"{artifact_id}.json"
        sidecar_path.write_text("garbage")
        second = registry.get(artifact_id)
        assert second is not None
        assert second.artifact_id == artifact_id
        assert first == second
