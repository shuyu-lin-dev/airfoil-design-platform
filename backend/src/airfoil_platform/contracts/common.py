"""Common Pydantic contracts shared across all API endpoints."""

from typing import Optional
from pydantic import BaseModel, Field, model_validator

from airfoil_platform.config import settings


# ---- Result metadata ----

class StubMeta(BaseModel):
    is_stub: bool = True
    model_version: str = settings.STUB_MODEL_VERSION


# ---- 2D / 3D points ----

class Point2D(BaseModel):
    x: float
    y: float


class CpPoint(BaseModel):
    x: float
    y: float
    cp: float


# ---- CST params ----

CST_PARAMS_COUNT = 12


def validate_cst_params(v: list) -> list:
    if len(v) != CST_PARAMS_COUNT:
        raise ValueError(f"cst_params must have exactly {CST_PARAMS_COUNT} values, got {len(v)}")
    return v


# ---- Condition ----

class Condition(BaseModel):
    mach: float
    angle_of_attack: float


# ---- Wing planform ----

class WingPlanform(BaseModel):
    span: Optional[float] = settings.DEFAULT_WING_SPAN
    chord: Optional[float] = settings.DEFAULT_WING_CHORD

    @model_validator(mode="after")
    def apply_defaults_and_validate(self):
        if self.span is None:
            self.span = settings.DEFAULT_WING_SPAN
        if self.chord is None:
            self.chord = settings.DEFAULT_WING_CHORD
        if not (settings.SPAN_MIN < self.span <= settings.SPAN_MAX):
            raise ValueError(
                f"span must be in ({settings.SPAN_MIN}, {settings.SPAN_MAX}], got {self.span}"
            )
        if not (settings.CHORD_MIN < self.chord <= settings.CHORD_MAX):
            raise ValueError(
                f"chord must be in ({settings.CHORD_MIN}, {settings.CHORD_MAX}], got {self.chord}"
            )
        return self


# ---- Structure design ----

class StructureDesign(BaseModel):
    rear_spar_web_thickness: float
    rib_thickness: float
    rib_spacing: float

    @model_validator(mode="after")
    def validate_ranges(self):
        if not (settings.REAR_SPAR_WEB_THICKNESS_MIN <= self.rear_spar_web_thickness <=
                settings.REAR_SPAR_WEB_THICKNESS_MAX):
            raise ValueError(
                f"rear_spar_web_thickness must be in "
                f"[{settings.REAR_SPAR_WEB_THICKNESS_MIN}, {settings.REAR_SPAR_WEB_THICKNESS_MAX}]"
            )
        if not (settings.RIB_THICKNESS_MIN <= self.rib_thickness <= settings.RIB_THICKNESS_MAX):
            raise ValueError(
                f"rib_thickness must be in "
                f"[{settings.RIB_THICKNESS_MIN}, {settings.RIB_THICKNESS_MAX}]"
            )
        if not (settings.RIB_SPACING_MIN <= self.rib_spacing <= settings.RIB_SPACING_MAX):
            raise ValueError(
                f"rib_spacing must be in "
                f"[{settings.RIB_SPACING_MIN}, {settings.RIB_SPACING_MAX}]"
            )
        return self


# ---- Material properties ----

class MaterialGroup(BaseModel):
    elastic_modulus: float = Field(gt=0)
    material_density: float = Field(gt=0)


class MaterialProperties(BaseModel):
    skin: Optional[MaterialGroup] = None
    internal_structure: Optional[MaterialGroup] = None

    def get_skin(self) -> MaterialGroup:
        if self.skin is not None:
            return self.skin
        return MaterialGroup(
            elastic_modulus=settings.DEFAULT_SKIN_ELASTIC_MODULUS_PA,
            material_density=settings.DEFAULT_SKIN_MATERIAL_DENSITY_KG_M3,
        )

    def get_internal_structure(self) -> MaterialGroup:
        if self.internal_structure is not None:
            return self.internal_structure
        return MaterialGroup(
            elastic_modulus=settings.DEFAULT_INTERNAL_STRUCTURE_ELASTIC_MODULUS_PA,
            material_density=settings.DEFAULT_INTERNAL_STRUCTURE_MATERIAL_DENSITY_KG_M3,
        )


# ---- Ratio validation ----

def validate_ratio(v: float) -> float:
    if not (0 < v <= 1):
        raise ValueError(f"ratio must be in (0, 1], got {v}")
    return v


# ---- Teaching control point ----

class TeachingControlPoint(BaseModel):
    x: float = Field(ge=0, le=1)
    y: float
