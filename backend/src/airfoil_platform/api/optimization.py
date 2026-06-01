from __future__ import annotations

from fastapi import APIRouter

from airfoil_platform.contracts.optimization import (
    AeroOptimizationRequest,
    AeroOptimizationResponse,
    CoupledOptimizationRequest,
    CoupledOptimizationResponse,
    StructOptimizationRequest,
    StructOptimizationResponse,
)
from airfoil_platform.services.optimization_service import (
    optimize_aero,
    optimize_coupled,
    optimize_struct,
)

router = APIRouter(prefix="/optimization", tags=["optimization"])


@router.post("/aerodynamic", response_model=AeroOptimizationResponse)
async def aerodynamic_optimization(request: AeroOptimizationRequest) -> AeroOptimizationResponse:
    return optimize_aero(request)


@router.post("/structural", response_model=StructOptimizationResponse)
async def structural_optimization(request: StructOptimizationRequest) -> StructOptimizationResponse:
    return optimize_struct(request)


@router.post("/coupled", response_model=CoupledOptimizationResponse)
async def coupled_optimization(request: CoupledOptimizationRequest) -> CoupledOptimizationResponse:
    return optimize_coupled(request)
