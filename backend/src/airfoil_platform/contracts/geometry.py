from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from airfoil_platform.contracts.common import ResultMeta, validate_cst_12


class Airfoil2DRequest(BaseModel):
    cst_params: Annotated[list[float], Field(min_length=12, max_length=12), AfterValidator(validate_cst_12)]


class AirfoilPoint(BaseModel):
    x: float
    y: float


class Airfoil2DResponse(BaseModel):
    points: list[AirfoilPoint] = Field(min_length=200, max_length=200)
    is_stub: bool = True
    model_version: str = "stub-v0"
