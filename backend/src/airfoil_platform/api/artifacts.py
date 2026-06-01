from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from airfoil_platform.config.settings import ARTIFACT_ROOT
from airfoil_platform.contracts.artifacts import ArtifactMetadataResponse

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

_artifact_root = ARTIFACT_ROOT


def _role_dirs() -> list[str]:
    return ["aerodynamic", "geometry"]


def _find_sidecar(artifact_id: str) -> Path | None:
    base = Path(_artifact_root)
    for role_dir in _role_dirs():
        sidecar = base / role_dir / f"{artifact_id}.json"
        if sidecar.exists():
            return sidecar
    return None


def _find_artifact_file(artifact_id: str) -> Path | None:
    base = Path(_artifact_root)
    for role_dir in _role_dirs():
        for ext in (".h5", ".step"):
            file_path = base / role_dir / f"{artifact_id}{ext}"
            if file_path.exists():
                return file_path
    return None


@router.get("/{artifact_id}", response_model=ArtifactMetadataResponse)
async def get_artifact_metadata(artifact_id: str) -> ArtifactMetadataResponse:
    sidecar = _find_sidecar(artifact_id)
    if sidecar is None:
        raise HTTPException(status_code=404, detail=f"Artifact '{artifact_id}' not found")
    return ArtifactMetadataResponse(**json.loads(sidecar.read_text()))


@router.get("/{artifact_id}/download")
async def download_artifact(artifact_id: str):
    file_path = _find_artifact_file(artifact_id)
    if file_path is None:
        raise HTTPException(status_code=404, detail=f"Artifact '{artifact_id}' not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_path.name)
