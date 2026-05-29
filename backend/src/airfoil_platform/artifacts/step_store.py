"""STEP artifact storage for structural geometry files."""

import os

from airfoil_platform.artifacts.artifact_registry import (
    artifact_file_path,
    write_sidecar,
    build_metadata,
    read_sidecar,
)


def write_step_artifact(
    artifact_id: str,
    step_content: bytes,
    components: list,
) -> str:
    """Write a STEP file and its JSON sidecar. Returns the file path."""
    file_path = artifact_file_path("geometry", artifact_id, "step")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(step_content)

    meta = build_metadata(
        artifact_id=artifact_id,
        format="step",
        role="structural_step",
        file_path=file_path,
        components=components,
    )
    write_sidecar(artifact_id, "geometry", meta)

    return file_path


def export_cad_entity_as_step(workplane_obj) -> bytes:
    """Export a CadQuery workplane object as STEP bytes."""
    import cadquery as cq
    import tempfile
    import shutil

    tmp_dir = tempfile.mkdtemp()
    tmp_step = os.path.join(tmp_dir, "export.step")
    try:
        cq.exporters.export(workplane_obj, tmp_step)
        with open(tmp_step, "rb") as f:
            return f.read()
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def import_step_and_get_components(file_path: str) -> list:
    """Import a STEP file and return the names of top-level solids/shapes."""
    import cadquery as cq

    result = cq.importers.importStep(file_path)
    if result is None:
        return []
    if hasattr(result, "vals"):
        shapes = result.vals()
    elif hasattr(result, "Solids"):
        shapes = result.Solids()
    else:
        return []
    return [s for s in shapes if s is not None]


def get_step_metadata(artifact_id: str) -> dict:
    """Read STEP artifact metadata from its JSON sidecar."""
    return read_sidecar("geometry", artifact_id)
