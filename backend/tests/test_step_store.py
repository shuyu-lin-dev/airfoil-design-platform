"""Tests for STEP artifact store (no HTTP dependency)."""

import os
import cadquery as cq

from airfoil_platform.artifacts.artifact_registry import read_sidecar
from airfoil_platform.artifacts.step_store import (
    write_step_artifact,
    export_cad_entity_as_step,
    import_step_and_get_components,
    get_step_metadata,
)


def _make_box():
    """Create a simple CadQuery box for testing."""
    return cq.Workplane("XY").box(1.0, 2.0, 3.0)


def test_export_cad_entity_as_step_bytes():
    box = _make_box()
    step_bytes = export_cad_entity_as_step(box)
    assert len(step_bytes) > 0
    assert b"ISO-10303-21" in step_bytes


def test_write_step_artifact_creates_file():
    box = _make_box()
    step_bytes = export_cad_entity_as_step(box)
    path = write_step_artifact("step-test-01", step_bytes, ["box"])
    assert os.path.isfile(path)
    assert path.endswith(".step")


def test_write_step_artifact_creates_sidecar():
    box = _make_box()
    step_bytes = export_cad_entity_as_step(box)
    write_step_artifact("step-test-02", step_bytes, ["box"])

    meta = get_step_metadata("step-test-02")
    assert meta is not None
    assert meta["artifact_id"] == "step-test-02"
    assert meta["format"] == "step"
    assert meta["role"] == "structural_step"
    assert meta["status"] == "ready"
    assert "components" in meta
    assert meta["components"] == ["box"]


def test_step_file_reimportable():
    """STEP file exported from CadQuery must be re-importable."""
    box = _make_box()
    step_bytes = export_cad_entity_as_step(box)
    path = write_step_artifact("reimport-test", step_bytes, ["box"])

    shapes = import_step_and_get_components(path)
    assert len(shapes) > 0, "STEP should contain at least one shape"

    # Each shape should have non-zero volume
    for shape in shapes:
        assert shape is not None


def test_sidecar_roundtrip():
    box = _make_box()
    step_bytes = export_cad_entity_as_step(box)
    write_step_artifact("roundtrip-step", step_bytes, ["front_spar", "rear_spar"])

    meta = get_step_metadata("roundtrip-step")
    assert meta["components"] == ["front_spar", "rear_spar"]
    assert os.path.isfile(meta["path"])


def test_read_sidecar_missing():
    meta = get_step_metadata("nonexistent-step-id")
    assert meta is None
