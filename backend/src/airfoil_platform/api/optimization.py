"""Optimization API routes."""

from fastapi import APIRouter

from airfoil_platform.contracts.optimization import (
    AeroOptRequest, AeroOptResponse,
    StructOptRequest, StructOptResponse,
    CoupledOptRequest, CoupledOptResponse,
)
from airfoil_platform.services.optimization_service import (
    aerodynamic_optimization_service,
    structural_optimization_service,
    coupled_optimization_service,
)

router = APIRouter(prefix="/optimization", tags=["optimization"])


@router.post("/aerodynamic", response_model=AeroOptResponse)
async def aero_optimize(request: AeroOptRequest):
    return aerodynamic_optimization_service(
        cst_params=request.cst_params,
        mach=request.condition.mach,
        aoa=request.condition.angle_of_attack,
        target=request.target_improvement_ratio,
    )


@router.post("/structural", response_model=StructOptResponse)
async def struct_optimize(request: StructOptRequest):
    mp = request.material_properties
    return structural_optimization_service(
        cst_params=request.cst_params,
        mach=request.condition.mach,
        aoa=request.condition.angle_of_attack,
        span=request.wing_planform.span,
        chord=request.wing_planform.chord,
        rear_spar=request.structure_design.rear_spar_web_thickness,
        rib_t=request.structure_design.rib_thickness,
        rib_s=request.structure_design.rib_spacing,
        skin_mat=mp.get_skin(),
        internal_mat=mp.get_internal_structure(),
        target=request.target_reduction_ratio,
    )


@router.post("/coupled", response_model=CoupledOptResponse)
async def coupled_optimize(request: CoupledOptRequest):
    mp = request.material_properties
    return coupled_optimization_service(
        cst_params=request.cst_params,
        mach=request.condition.mach,
        aoa=request.condition.angle_of_attack,
        span=request.wing_planform.span,
        chord=request.wing_planform.chord,
        rear_spar=request.structure_design.rear_spar_web_thickness,
        rib_t=request.structure_design.rib_thickness,
        rib_s=request.structure_design.rib_spacing,
        skin_mat=mp.get_skin(),
        internal_mat=mp.get_internal_structure(),
        target=request.target_improvement_ratio,
    )
