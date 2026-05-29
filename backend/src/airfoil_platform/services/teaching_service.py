"""Teaching service: orchestrates teaching workflows."""

from airfoil_platform.contracts.teaching import (
    AirfoilFromControlPointsResponse,
    CstFromAirfoilResponse,
)
from airfoil_platform.core.teaching import generate_teaching_airfoil, inverse_cst_from_airfoil


def teaching_airfoil_service() -> AirfoilFromControlPointsResponse:
    points = generate_teaching_airfoil()
    return AirfoilFromControlPointsResponse(points=points)


def teaching_cst_inverse_service(points: list) -> CstFromAirfoilResponse:
    cst_params = inverse_cst_from_airfoil(points)
    return CstFromAirfoilResponse(cst_params=cst_params)
