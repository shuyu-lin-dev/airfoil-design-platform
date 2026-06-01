from __future__ import annotations

from fastapi import APIRouter

from airfoil_platform.contracts.structure import (
    StructurePredictionRequest,
    StructurePredictionResponse,
)
from airfoil_platform.services.structure_service import predict

router = APIRouter(prefix="/structure", tags=["structure"])


@router.post("/predict", response_model=StructurePredictionResponse)
async def structure_predict(request: StructurePredictionRequest) -> StructurePredictionResponse:
    return predict(request)
