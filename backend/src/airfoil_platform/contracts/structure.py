from __future__ import annotations

from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, Field

from airfoil_platform.contracts.common import (
    ConditionParams,
    MaterialProperties,
    StructureDesign,
    WingPlanform,
    validate_cst_12,
)


class StructurePredictionRequest(BaseModel):
    cst_params: Annotated[list[float], Field(min_length=12, max_length=12), AfterValidator(validate_cst_12)]
    wing_planform: WingPlanform
    structure_design: StructureDesign
    condition: ConditionParams
    material_properties: Optional[MaterialProperties] = None


class StructurePredictionResponse(BaseModel):
    max_stress: float
    weight: float
    is_stub: bool = True
    model_version: str = "stub-v0"
