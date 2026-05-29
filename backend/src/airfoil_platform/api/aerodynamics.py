"""Aerodynamics API routes."""

from fastapi import APIRouter

from airfoil_platform.contracts.aerodynamics import (
    AerodynamicPredictRequest,
    AerodynamicPredictResponse,
)
from airfoil_platform.services.aerodynamic_service import predict_aerodynamic_service

router = APIRouter(prefix="/aerodynamics", tags=["aerodynamics"])


@router.post("/predict", response_model=AerodynamicPredictResponse)
async def predict(request: AerodynamicPredictRequest):
    return predict_aerodynamic_service(
        request.cst_params,
        request.condition.mach,
        request.condition.angle_of_attack,
    )
