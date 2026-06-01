from __future__ import annotations

from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, Field

from airfoil_platform.contracts.artifacts import ArtifactMetadataResponse
from airfoil_platform.contracts.common import (
    MaterialProperties,
    ResultMeta,
    StructureDesign,
    WingPlanform,
    validate_cst_12,
)


class Airfoil2DRequest(BaseModel):
    cst_params: Annotated[list[float], Field(min_length=12, max_length=12), AfterValidator(validate_cst_12)]


class AirfoilPoint(BaseModel):
    x: float
    y: float


class Airfoil2DResponse(BaseModel):
    points: list[AirfoilPoint] = Field(min_length=200, max_length=200)
    is_stub: bool = True
    model_version: str = "stub-v0"


# ── 3D wing (T008) ──

class Wing3DRequest(BaseModel):
    cst_params: Annotated[list[float], Field(min_length=12, max_length=12), AfterValidator(validate_cst_12)]
    wing_planform: WingPlanform
    structure_design: StructureDesign
    material_properties: Optional[MaterialProperties] = None


class Wing3DResponse(BaseModel):
    geometry_artifact: ArtifactMetadataResponse
    is_stub: bool = True
    model_version: str = "stub-v0"
