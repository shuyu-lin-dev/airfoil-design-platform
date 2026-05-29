"""Contracts for structure prediction endpoint."""

from typing import List, Optional
from pydantic import BaseModel, field_validator

from airfoil_platform.contracts.common import (
    Condition,
    WingPlanform,
    StructureDesign,
    MaterialProperties,
    validate_cst_params,
)


class StructurePredictRequest(BaseModel):
    cst_params: List[float]
    condition: Condition
    wing_planform: WingPlanform = WingPlanform()
    structure_design: StructureDesign
    material_properties: MaterialProperties = MaterialProperties()

    @field_validator("cst_params")
    @classmethod
    def check_length(cls, v):
        return validate_cst_params(v)


class StructurePredictResponse(BaseModel):
    max_stress: float
    weight: float
    is_stub: bool = True
    model_version: str = "stub-v0"
