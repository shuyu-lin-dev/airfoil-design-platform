"""Contracts for teaching API endpoints."""

from typing import List
from pydantic import BaseModel, field_validator

from airfoil_platform.contracts.common import (
    Point2D,
    TeachingControlPoint,
    validate_cst_params,
)


class AirfoilFromControlPointsRequest(BaseModel):
    camber_control_points: List[TeachingControlPoint]
    thickness_control_points: List[TeachingControlPoint]

    @field_validator("camber_control_points", "thickness_control_points")
    @classmethod
    def check_two_points(cls, v):
        if len(v) != 2:
            raise ValueError(f"Must have exactly 2 control points, got {len(v)}")
        return v


class AirfoilFromControlPointsResponse(BaseModel):
    points: List[Point2D]
    is_stub: bool = True
    model_version: str = "stub-v0"


class CstFromAirfoilRequest(BaseModel):
    points: List[Point2D]

    @field_validator("points")
    @classmethod
    def check_200_points(cls, v):
        if len(v) != 200:
            raise ValueError(f"Must have exactly 200 points, got {len(v)}")
        return v


class CstFromAirfoilResponse(BaseModel):
    cst_params: List[float]
    is_stub: bool = True
    model_version: str = "stub-v0"
