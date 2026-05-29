"""Contracts for optimization endpoints."""

from typing import List, Optional
from pydantic import BaseModel, field_validator

from airfoil_platform.contracts.common import (
    Condition,
    WingPlanform,
    StructureDesign,
    MaterialProperties,
    MaterialGroup,
    validate_cst_params,
    validate_ratio,
)


# ---- Aerodynamic optimization ----

class AeroOptRequest(BaseModel):
    cst_params: List[float]
    condition: Condition
    target_improvement_ratio: float

    @field_validator("cst_params")
    @classmethod
    def check_length(cls, v):
        return validate_cst_params(v)

    @field_validator("target_improvement_ratio")
    @classmethod
    def check_ratio(cls, v):
        return validate_ratio(v)


class AeroOptOriginal(BaseModel):
    cst_params: List[float]
    condition: Condition
    lift_drag_ratio: float


class AeroOptOptimized(BaseModel):
    cst_params: List[float]
    condition: Condition
    lift_drag_ratio: float


class AeroOptResponse(BaseModel):
    original: AeroOptOriginal
    optimized: AeroOptOptimized
    actual_improvement_ratio: float
    is_stub: bool = True
    model_version: str = "stub-v0"


# ---- Structural optimization ----

class StructOptRequest(BaseModel):
    cst_params: List[float]
    condition: Condition
    wing_planform: WingPlanform = WingPlanform()
    structure_design: StructureDesign
    material_properties: MaterialProperties = MaterialProperties()
    target_reduction_ratio: float

    @field_validator("cst_params")
    @classmethod
    def check_length(cls, v):
        return validate_cst_params(v)

    @field_validator("target_reduction_ratio")
    @classmethod
    def check_ratio(cls, v):
        return validate_ratio(v)


class StructOptOriginal(BaseModel):
    cst_params: List[float]
    condition: Condition
    wing_planform: WingPlanform
    structure_design: StructureDesign
    material_properties: MaterialProperties
    weight: float


class StructOptOptimized(BaseModel):
    cst_params: List[float]
    condition: Condition
    wing_planform: WingPlanform
    structure_design: StructureDesign
    material_properties: MaterialProperties
    weight: float


class StructOptResponse(BaseModel):
    original: StructOptOriginal
    optimized: StructOptOptimized
    actual_reduction_ratio: float
    is_stub: bool = True
    model_version: str = "stub-v0"


# ---- Coupled optimization ----

class CoupledOptRequest(BaseModel):
    cst_params: List[float]
    condition: Condition
    wing_planform: WingPlanform = WingPlanform()
    structure_design: StructureDesign
    material_properties: MaterialProperties = MaterialProperties()
    target_improvement_ratio: float

    @field_validator("cst_params")
    @classmethod
    def check_length(cls, v):
        return validate_cst_params(v)

    @field_validator("target_improvement_ratio")
    @classmethod
    def check_ratio(cls, v):
        return validate_ratio(v)


class CoupledOptOriginal(BaseModel):
    cst_params: List[float]
    condition: Condition
    wing_planform: WingPlanform
    structure_design: StructureDesign
    material_properties: MaterialProperties
    weight: float
    lift_drag_ratio: float
    fitness: float


class CoupledOptOptimized(BaseModel):
    cst_params: List[float]
    condition: Condition
    wing_planform: WingPlanform
    structure_design: StructureDesign
    material_properties: MaterialProperties
    weight: float
    lift_drag_ratio: float
    fitness: float


class CoupledOptResponse(BaseModel):
    original: CoupledOptOriginal
    optimized: CoupledOptOptimized
    actual_improvement_ratio: float
    is_stub: bool = True
    model_version: str = "stub-v0"
