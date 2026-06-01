import json
from pathlib import Path

import cadquery as cq


def write_step_artifact(
    artifact_id: str,
    shape,
    components: list[str],
    artifact_root: str,
) -> dict:
    role_dir = Path(artifact_root) / "geometry"
    role_dir.mkdir(parents=True, exist_ok=True)

    step_path = role_dir / f"{artifact_id}.step"
    cq.exporters.export(shape, str(step_path))

    sidecar = {
        "artifact_id": artifact_id,
        "format": "step",
        "role": "structural_step",
        "path": str(step_path),
        "status": "ready",
        "components": components,
    }
    sidecar_path = role_dir / f"{artifact_id}.json"
    sidecar_path.write_text(json.dumps(sidecar, indent=2))

    return sidecar
