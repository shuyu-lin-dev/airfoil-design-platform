import hashlib
import json
from pathlib import Path

import h5py
import numpy as np


def generate_artifact_id(params: dict) -> str:
    canonical = json.dumps(params, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]


def write_hdf5_artifact(
    artifact_id: str,
    coordinates: np.ndarray,
    pressure: np.ndarray,
    velocity: np.ndarray,
    artifact_root: str,
) -> dict:
    role_dir = Path(artifact_root) / "aerodynamic"
    role_dir.mkdir(parents=True, exist_ok=True)

    h5_path = role_dir / f"{artifact_id}.h5"
    with h5py.File(h5_path, "w") as f:
        f.create_dataset("/coordinates", data=coordinates)
        f.create_dataset("/fields/pressure", data=pressure)
        f.create_dataset("/fields/velocity", data=velocity)

    sidecar = {
        "artifact_id": artifact_id,
        "format": "hdf5",
        "role": "aerodynamic",
        "path": str(h5_path),
        "status": "ready",
        "datasets": ["/coordinates", "/fields/pressure", "/fields/velocity"],
    }
    sidecar_path = role_dir / f"{artifact_id}.json"
    sidecar_path.write_text(json.dumps(sidecar, indent=2))

    return sidecar
