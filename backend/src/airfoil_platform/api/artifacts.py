"""Artifact query and download API routes."""

import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from airfoil_platform.artifacts.artifact_registry import artifact_dir, read_sidecar

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

CATEGORIES = ["aerodynamic", "geometry"]


def _find_sidecar(artifact_id: str) -> tuple:
    """Find sidecar metadata and category for a given artifact_id."""
    for cat in CATEGORIES:
        meta = read_sidecar(cat, artifact_id)
        if meta is not None:
            return meta, cat
    raise HTTPException(status_code=404, detail={
        "error": {
            "code": "ARTIFACT_NOT_FOUND",
            "message": f"Artifact {artifact_id} not found.",
            "resolution": "请确认 artifact_id 是否正确，或先生成对应的 artifact。",
        }
    })


@router.get("/{artifact_id}")
async def get_artifact_meta(artifact_id: str):
    meta, _ = _find_sidecar(artifact_id)
    return meta


@router.get("/{artifact_id}/download")
async def download_artifact(artifact_id: str):
    meta, _ = _find_sidecar(artifact_id)
    file_path = meta.get("path", "")
    if not file_path or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail={
            "error": {
                "code": "FILE_NOT_FOUND",
                "message": f"Artifact file for {artifact_id} not found on disk.",
                "resolution": "文件可能已被移动或删除，请重新生成 artifact。",
            }
        })
    return FileResponse(file_path, filename=os.path.basename(file_path))
