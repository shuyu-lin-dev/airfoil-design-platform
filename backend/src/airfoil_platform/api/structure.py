"""Structure API routes."""

from fastapi import APIRouter

from airfoil_platform.contracts.structure import (
    StructurePredictRequest,
    StructurePredictResponse,
)
from airfoil_platform.services.structure_service import predict_structure_service

router = APIRouter(prefix="/structure", tags=["structure"])


@router.post("/predict", response_model=StructurePredictResponse)
async def predict(request: StructurePredictRequest):
    mp = request.material_properties
    return predict_structure_service(
        cst_params=request.cst_params,
        span=request.wing_planform.span,
        chord=request.wing_planform.chord,
        rear_spar_web_thickness=request.structure_design.rear_spar_web_thickness,
        rib_thickness=request.structure_design.rib_thickness,
        rib_spacing=request.structure_design.rib_spacing,
        skin_material=mp.get_skin(),
        internal_material=mp.get_internal_structure(),
    )
