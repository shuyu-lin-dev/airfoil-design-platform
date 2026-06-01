from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from airfoil_platform.contracts.common import validate_cst_12


class ControlPoint(BaseModel):
    x: float
    y: float


class AirfoilFromControlPointsRequest(BaseModel):
    camber_control_points: list[ControlPoint] = Field(min_length=2, max_length=2)
    thickness_control_points: list[ControlPoint] = Field(min_length=2, max_length=2)


class AirfoilFromControlPointsResponse(BaseModel):
    points: list[dict] = Field(min_length=200, max_length=200)
    is_stub: bool = True
    model_version: str = "stub-v0"


class CstFromAirfoilRequest(BaseModel):
    points: list[dict] = Field(min_length=200, max_length=200)


class CstFromAirfoilResponse(BaseModel):
    cst_params: list[float] = Field(min_length=12, max_length=12)
    is_stub: bool = True
    model_version: str = "stub-v0"
