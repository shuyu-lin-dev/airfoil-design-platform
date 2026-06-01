import json
import tempfile
from pathlib import Path

import cadquery as cq

from airfoil_platform.artifacts.artifact_registry import ArtifactRegistry
from airfoil_platform.artifacts.step_store import write_step_artifact


def _make_test_box():
    return cq.Workplane("XY").box(1.0, 2.0, 3.0)


class TestStepStore:

    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.box = _make_test_box()

    def teardown_method(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_write_step_and_sidecar(self):
        artifact_id = "step123456789"
        components = ["skin"]
        meta = write_step_artifact(
            artifact_id=artifact_id,
            shape=self.box,
            components=components,
            artifact_root=self.tmpdir,
        )

        # STEP file exists
        step_path = Path(self.tmpdir) / "geometry" / f"{artifact_id}.step"
        assert step_path.exists()
        assert step_path.stat().st_size > 0

        # JSON sidecar exists with correct fields
        sidecar_path = Path(self.tmpdir) / "geometry" / f"{artifact_id}.json"
        assert sidecar_path.exists()
        sidecar = json.loads(sidecar_path.read_text())
        assert sidecar["artifact_id"] == artifact_id
        assert sidecar["format"] == "step"
        assert sidecar["role"] == "structural_step"
        assert sidecar["status"] == "ready"
        assert sidecar["components"] == components

        # Returned metadata matches
        assert meta["artifact_id"] == artifact_id
        assert meta["format"] == "step"

    def test_creates_directories_if_missing(self):
        deep_root = Path(self.tmpdir) / "nested" / "deep"
        artifact_id = "deepstep12345"
        meta = write_step_artifact(
            artifact_id=artifact_id,
            shape=self.box,
            components=["front_spar"],
            artifact_root=str(deep_root),
        )
        step_path = deep_root / "geometry" / f"{artifact_id}.step"
        assert step_path.exists()
        assert meta["status"] == "ready"

    def test_step_can_be_re_imported(self):
        """STEP file written by write_step_artifact can be re-imported by cadquery."""
        artifact_id = "reimport00000"
        _meta = write_step_artifact(
            artifact_id=artifact_id,
            shape=self.box,
            components=["skin"],
            artifact_root=self.tmpdir,
        )
        step_path = Path(self.tmpdir) / "geometry" / f"{artifact_id}.step"
        imported = cq.importers.importStep(str(step_path))
        assert imported is not None
        bbox = imported.findSolid().BoundingBox()
        assert abs(bbox.xlen - 1.0) < 0.01
        assert abs(bbox.ylen - 2.0) < 0.01
        assert abs(bbox.zlen - 3.0) < 0.01


class TestStepArtifactRegistry:
    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.box = _make_test_box()

    def teardown_method(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_registry_can_query_step_sidecar(self):
        artifact_id = "registry12345"
        write_step_artifact(
            artifact_id=artifact_id,
            shape=self.box,
            components=["skin", "front_spar"],
            artifact_root=self.tmpdir,
        )

        registry = ArtifactRegistry(self.tmpdir)
        retrieved = registry.get(artifact_id)
        assert retrieved is not None
        assert retrieved.artifact_id == artifact_id
        assert retrieved.format == "step"
        assert retrieved.role == "structural_step"
        assert retrieved.status == "ready"
        assert "skin" in retrieved.components
        assert "front_spar" in retrieved.components
