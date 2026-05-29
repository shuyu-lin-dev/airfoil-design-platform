"""Format-agnostic artifact metadata registry.

Uses on-disk JSON sidecars as the source of truth so lookups survive restarts.
"""

import os
import json
from typing import Optional, Dict


def artifact_dir() -> str:
    from airfoil_platform.config.settings import ARTIFACT_ROOT
    root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "runtime_artifacts"))
    if not os.path.isabs(root):
        root = os.path.abspath(root)
    return root


def _sidecar_path(artifact_root: str, category: str, artifact_id: str) -> str:
    return os.path.join(artifact_root, category, f"{artifact_id}.json")


def write_sidecar(artifact_id: str, category: str, metadata: dict) -> str:
    """Write JSON sidecar and return its path."""
    root = artifact_dir()
    cat_dir = os.path.join(root, category)
    os.makedirs(cat_dir, exist_ok=True)
    sp = _sidecar_path(root, category, artifact_id)
    with open(sp, "w") as f:
        json.dump(metadata, f, indent=2)
    return sp


def read_sidecar(category: str, artifact_id: str) -> Optional[dict]:
    """Read JSON sidecar from disk."""
    root = artifact_dir()
    sp = _sidecar_path(root, category, artifact_id)
    if not os.path.isfile(sp):
        return None
    with open(sp, "r") as f:
        return json.load(f)


def build_metadata(
    artifact_id: str,
    format: str,
    role: str,
    file_path: str,
    status: str = "ready",
    datasets: Optional[dict] = None,
    components: Optional[list] = None,
) -> dict:
    meta = {
        "artifact_id": artifact_id,
        "format": format,
        "role": role,
        "path": file_path,
        "status": status,
    }
    if datasets is not None:
        meta["datasets"] = datasets
    if components is not None:
        meta["components"] = components
    return meta


def artifact_file_path(category: str, artifact_id: str, extension: str) -> str:
    root = artifact_dir()
    return os.path.join(root, category, f"{artifact_id}.{extension}")
