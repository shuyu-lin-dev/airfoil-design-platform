from __future__ import annotations

from fastapi import APIRouter

from airfoil_platform.config.settings import ARTIFACT_ROOT
from airfoil_platform.contracts.geometry import (
    Airfoil2DRequest,
    Airfoil2DResponse,
    Wing3DRequest,
    Wing3DResponse,
)
from airfoil_platform.services.geometry_service import generate_airfoil_2d, generate_wing_3d

router = APIRouter(prefix="/geometry", tags=["geometry"])

_artifact_root = ARTIFACT_ROOT


@router.post("/airfoil-2d", response_model=Airfoil2DResponse)
async def airfoil_2d(request: Airfoil2DRequest) -> Airfoil2DResponse:
    return generate_airfoil_2d(request)


@router.post("/wing-3d", response_model=Wing3DResponse)
async def wing_3d(request: Wing3DRequest) -> Wing3DResponse:
    return generate_wing_3d(request, artifact_root=_artifact_root)
