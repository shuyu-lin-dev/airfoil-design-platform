from __future__ import annotations

from fastapi import APIRouter

from airfoil_platform.config.settings import ARTIFACT_ROOT
from airfoil_platform.contracts.aerodynamics import (
    AerodynamicPredictionRequest,
    AerodynamicPredictionResponse,
)
from airfoil_platform.services.aerodynamic_service import predict

router = APIRouter(prefix="/aerodynamics", tags=["aerodynamics"])

_artifact_root = ARTIFACT_ROOT


@router.post("/predict", response_model=AerodynamicPredictionResponse)
async def aerodynamic_predict(request: AerodynamicPredictionRequest) -> AerodynamicPredictionResponse:
    return predict(request, artifact_root=_artifact_root)
