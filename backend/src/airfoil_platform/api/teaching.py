from __future__ import annotations

from fastapi import APIRouter

from airfoil_platform.contracts.teaching import (
    AirfoilFromControlPointsRequest,
    AirfoilFromControlPointsResponse,
    CstFromAirfoilRequest,
    CstFromAirfoilResponse,
)
from airfoil_platform.services.teaching_service import (
    cst_from_airfoil,
    generate_from_control_points,
)

router = APIRouter(prefix="/teaching", tags=["teaching"])


@router.post("/airfoil-from-control-points", response_model=AirfoilFromControlPointsResponse)
async def airfoil_from_control_points(
    request: AirfoilFromControlPointsRequest,
) -> AirfoilFromControlPointsResponse:
    return generate_from_control_points(request)


@router.post("/cst-from-airfoil", response_model=CstFromAirfoilResponse)
async def cst_from_airfoil_endpoint(request: CstFromAirfoilRequest) -> CstFromAirfoilResponse:
    return cst_from_airfoil(request)
