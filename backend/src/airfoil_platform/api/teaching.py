"""Teaching API routes."""

from fastapi import APIRouter

from airfoil_platform.contracts.teaching import (
    AirfoilFromControlPointsRequest,
    AirfoilFromControlPointsResponse,
    CstFromAirfoilRequest,
    CstFromAirfoilResponse,
)
from airfoil_platform.services.teaching_service import (
    teaching_airfoil_service,
    teaching_cst_inverse_service,
)

router = APIRouter(prefix="/teaching", tags=["teaching"])


@router.post("/airfoil-from-control-points", response_model=AirfoilFromControlPointsResponse)
async def airfoil_from_control_points(request: AirfoilFromControlPointsRequest):
    return teaching_airfoil_service()


@router.post("/cst-from-airfoil", response_model=CstFromAirfoilResponse)
async def cst_from_airfoil(request: CstFromAirfoilRequest):
    return teaching_cst_inverse_service(request.points)
