from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from airfoil_platform.contracts.artifacts import ArtifactMetadataResponse
from airfoil_platform.contracts.common import ConditionParams, ResultMeta, validate_cst_12


class AerodynamicPredictionRequest(BaseModel):
    cst_params: Annotated[list[float], Field(min_length=12, max_length=12), AfterValidator(validate_cst_12)]
    condition: ConditionParams


class CpPoint(BaseModel):
    x: float
    cp: float


class AerodynamicPredictionResponse(BaseModel):
    lift_drag_ratio: float
    cp_distribution: list[CpPoint] = Field(min_length=200, max_length=200)
    field_artifact: ArtifactMetadataResponse
    is_stub: bool = True
    model_version: str = "stub-v0"
