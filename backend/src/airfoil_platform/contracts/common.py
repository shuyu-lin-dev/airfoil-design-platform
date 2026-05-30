from typing import Optional

from pydantic import BaseModel, Field, field_validator

from airfoil_platform.config.settings import (
    DEFAULT_WING_SPAN,
    DEFAULT_WING_CHORD,
    SPAN_MAX,
    CHORD_MAX,
    REAR_SPAR_WEB_THICKNESS_MIN,
    REAR_SPAR_WEB_THICKNESS_MAX,
    RIB_THICKNESS_MIN,
    RIB_THICKNESS_MAX,
    RIB_SPACING_MIN,
    RIB_SPACING_MAX,
    STUB_MODEL_VERSION,
)


def validate_cst_12(v: list[float]) -> list[float]:
    if len(v) != 12:
        raise ValueError(f"cst_params must have exactly 12 values, got {len(v)}")
    return v


def validate_ratio(v: float) -> float:
    if not (0 < v <= 1):
        raise ValueError(f"ratio must be 0 < ratio <= 1, got {v}")
    return v


class WingPlanform(BaseModel):
    span: float = Field(default=DEFAULT_WING_SPAN)
    chord: float = Field(default=DEFAULT_WING_CHORD)

    @field_validator("span")
    @classmethod
    def span_range(cls, v: float) -> float:
        if not (0 < v <= SPAN_MAX):
            raise ValueError(f"span must be 0 < span <= {SPAN_MAX}, got {v}")
        return v

    @field_validator("chord")
    @classmethod
    def chord_range(cls, v: float) -> float:
        if not (0 < v <= CHORD_MAX):
            raise ValueError(f"chord must be 0 < chord <= {CHORD_MAX}, got {v}")
        return v


class StructureDesign(BaseModel):
    rear_spar_web_thickness: float
    rib_thickness: float
    rib_spacing: float

    @field_validator("rear_spar_web_thickness")
    @classmethod
    def rear_spar_range(cls, v: float) -> float:
        if not (REAR_SPAR_WEB_THICKNESS_MIN <= v <= REAR_SPAR_WEB_THICKNESS_MAX):
            raise ValueError(
                f"rear_spar_web_thickness must be "
                f"{REAR_SPAR_WEB_THICKNESS_MIN} <= v <= {REAR_SPAR_WEB_THICKNESS_MAX}, got {v}"
            )
        return v

    @field_validator("rib_thickness")
    @classmethod
    def rib_thickness_range(cls, v: float) -> float:
        if not (RIB_THICKNESS_MIN <= v <= RIB_THICKNESS_MAX):
            raise ValueError(
                f"rib_thickness must be {RIB_THICKNESS_MIN} <= v <= {RIB_THICKNESS_MAX}, got {v}"
            )
        return v

    @field_validator("rib_spacing")
    @classmethod
    def rib_spacing_range(cls, v: float) -> float:
        if not (RIB_SPACING_MIN <= v <= RIB_SPACING_MAX):
            raise ValueError(
                f"rib_spacing must be {RIB_SPACING_MIN} <= v <= {RIB_SPACING_MAX}, got {v}"
            )
        return v


class MaterialGroup(BaseModel):
    elastic_modulus: float
    material_density: float

    @field_validator("elastic_modulus", "material_density")
    @classmethod
    def positive_strict(cls, v: float) -> float:
        if v <= 0:
            raise ValueError(f"value must be strictly positive, got {v}")
        return v


class MaterialProperties(BaseModel):
    skin: Optional[MaterialGroup] = None
    internal_structure: Optional[MaterialGroup] = None


class ConditionParams(BaseModel):
    mach: float
    angle_of_attack: float


class ResultMeta(BaseModel):
    is_stub: bool = True
    model_version: str = STUB_MODEL_VERSION
