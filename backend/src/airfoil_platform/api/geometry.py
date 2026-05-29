"""Geometry API routes."""

from fastapi import APIRouter, HTTPException

from airfoil_platform.contracts.geometry import (
    Airfoil2DRequest,
    Airfoil2DResponse,
    Wing3DRequest,
    Wing3DResponse,
)
from airfoil_platform.services.geometry_service import (
    generate_airfoil_2d_service,
    generate_wing_3d_service,
)

router = APIRouter(prefix="/geometry", tags=["geometry"])


@router.post("/airfoil-2d", response_model=Airfoil2DResponse)
async def airfoil_2d(request: Airfoil2DRequest):
    return generate_airfoil_2d_service(request.cst_params)


@router.post("/wing-3d", response_model=Wing3DResponse)
async def wing_3d(request: Wing3DRequest):
    try:
        return generate_wing_3d_service(
            cst_params=request.cst_params,
            span=request.wing_planform.span,
            chord=request.wing_planform.chord,
            rear_spar_web_thickness=request.structure_design.rear_spar_web_thickness,
            rib_thickness=request.structure_design.rib_thickness,
            rib_spacing=request.structure_design.rib_spacing,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail={
            "error": {
                "code": "GEOMETRY_ERROR",
                "message": str(e),
                "resolution": "请调整 CST 参数使翼型厚度增加，或减少蒙皮厚度要求。",
            }
        })
