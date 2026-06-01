from __future__ import annotations

from airfoil_platform.contracts.teaching import (
    AirfoilFromControlPointsRequest,
    AirfoilFromControlPointsResponse,
    CstFromAirfoilRequest,
    CstFromAirfoilResponse,
)
from airfoil_platform.core.teaching import (
    approximate_cst_from_points,
    generate_airfoil_from_control_points,
)


def generate_from_control_points(request: AirfoilFromControlPointsRequest) -> AirfoilFromControlPointsResponse:
    camber = [cp.model_dump() for cp in request.camber_control_points]
    thickness = [cp.model_dump() for cp in request.thickness_control_points]
    upper, lower = generate_airfoil_from_control_points(camber, thickness)
    points = [{"x": p[0], "y": p[1]} for p in upper] + [{"x": p[0], "y": p[1]} for p in lower]
    return AirfoilFromControlPointsResponse(points=points)


def cst_from_airfoil(request: CstFromAirfoilRequest) -> CstFromAirfoilResponse:
    cst = approximate_cst_from_points(request.points)
    return CstFromAirfoilResponse(cst_params=cst)
