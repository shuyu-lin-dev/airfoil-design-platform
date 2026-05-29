"""Contracts for aerodynamic prediction endpoint."""

from typing import List, Dict
from pydantic import BaseModel, field_validator

from airfoil_platform.contracts.common import (
    CpPoint,
    Condition,
    validate_cst_params,
)


class AerodynamicPredictRequest(BaseModel):
    cst_params: List[float]
    condition: Condition

    @field_validator("cst_params")
    @classmethod
    def check_length(cls, v):
        return validate_cst_params(v)


class FieldArtifactMeta(BaseModel):
    artifact_id: str
    status: str
    format: str
    role: str
    path: str
    datasets: Dict[str, str]


class AerodynamicPredictResponse(BaseModel):
    lift_drag_ratio: float
    cp_distribution: List[CpPoint]
    field_artifact: FieldArtifactMeta
    is_stub: bool = True
    model_version: str = "stub-v0"
