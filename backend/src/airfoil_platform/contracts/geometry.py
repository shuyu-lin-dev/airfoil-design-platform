"""Contracts for geometry endpoints."""

from typing import List
from pydantic import BaseModel, field_validator

from airfoil_platform.contracts.common import (
    StubMeta,
    Point2D,
    WingPlanform,
    StructureDesign,
    validate_cst_params,
)


class Airfoil2DRequest(BaseModel):
    cst_params: List[float]

    @field_validator("cst_params")
    @classmethod
    def check_length(cls, v):
        return validate_cst_params(v)


class Airfoil2DResponse(BaseModel):
    points: List[Point2D]
    is_stub: bool = True
    model_version: str = "stub-v0"


class Wing3DRequest(BaseModel):
    cst_params: List[float]
    wing_planform: WingPlanform = WingPlanform()
    structure_design: StructureDesign

    @field_validator("cst_params")
    @classmethod
    def check_length(cls, v):
        return validate_cst_params(v)


class GeometryArtifactMeta(BaseModel):
    artifact_id: str
    status: str
    format: str
    role: str
    path: str
    components: List[str]


class Wing3DResponse(BaseModel):
    geometry_artifact: GeometryArtifactMeta
    is_stub: bool = True
    model_version: str = "stub-v0"
