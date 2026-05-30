from __future__ import annotations

from airfoil_platform.contracts.geometry import Airfoil2DRequest, Airfoil2DResponse, AirfoilPoint
from airfoil_platform.core.geometry import cst_to_airfoil_points


def generate_airfoil_2d(request: Airfoil2DRequest) -> Airfoil2DResponse:
    upper, lower = cst_to_airfoil_points(request.cst_params, n_points=100)
    points = [AirfoilPoint(x=pt[0], y=pt[1]) for pt in upper] + [
        AirfoilPoint(x=pt[0], y=pt[1]) for pt in lower
    ]
    return Airfoil2DResponse(points=points)
