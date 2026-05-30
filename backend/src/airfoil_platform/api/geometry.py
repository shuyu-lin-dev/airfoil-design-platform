from __future__ import annotations

from fastapi import APIRouter

from airfoil_platform.contracts.geometry import Airfoil2DRequest, Airfoil2DResponse
from airfoil_platform.services.geometry_service import generate_airfoil_2d

router = APIRouter(prefix="/geometry", tags=["geometry"])


@router.post("/airfoil-2d", response_model=Airfoil2DResponse)
async def airfoil_2d(request: Airfoil2DRequest) -> Airfoil2DResponse:
    return generate_airfoil_2d(request)
