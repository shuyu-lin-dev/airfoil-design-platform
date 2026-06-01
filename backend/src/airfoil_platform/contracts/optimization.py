from __future__ import annotations

from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, Field

from airfoil_platform.contracts.common import (
    ConditionParams,
    MaterialProperties,
    StructureDesign,
    WingPlanform,
    validate_cst_12,
    validate_ratio,
)


class AeroOptimizationRequest(BaseModel):
    cst_params: Annotated[list[float], Field(min_length=12, max_length=12), AfterValidator(validate_cst_12)]
    condition: ConditionParams
    target_improvement_ratio: Annotated[float, AfterValidator(validate_ratio)]


class AeroOptimizationResponse(BaseModel):
    original: list[float] = Field(min_length=12, max_length=12)
    optimized: list[float] = Field(min_length=12, max_length=12)
    actual_improvement_ratio: float
    is_stub: bool = True
    model_version: str = "stub-v0"


class StructOptimizationRequest(BaseModel):
    cst_params: Annotated[list[float], Field(min_length=12, max_length=12), AfterValidator(validate_cst_12)]
    wing_planform: WingPlanform
    structure_design: StructureDesign
    condition: ConditionParams
    target_reduction_ratio: Annotated[float, AfterValidator(validate_ratio)]
    material_properties: Optional[MaterialProperties] = None


class StructOptimizationResponse(BaseModel):
    original: StructureDesign
    optimized: StructureDesign
    actual_reduction_ratio: float
    is_stub: bool = True
    model_version: str = "stub-v0"


class CoupledOptimizationRequest(BaseModel):
    cst_params: Annotated[list[float], Field(min_length=12, max_length=12), AfterValidator(validate_cst_12)]
    wing_planform: WingPlanform
    structure_design: StructureDesign
    condition: ConditionParams
    target_improvement_ratio: Annotated[float, AfterValidator(validate_ratio)]
    material_properties: Optional[MaterialProperties] = None


class CoupledOptimizationResponse(BaseModel):
    original_cst: list[float] = Field(min_length=12, max_length=12)
    optimized_cst: list[float] = Field(min_length=12, max_length=12)
    original_structure: StructureDesign
    optimized_structure: StructureDesign
    actual_improvement_ratio: float
    is_stub: bool = True
    model_version: str = "stub-v0"
