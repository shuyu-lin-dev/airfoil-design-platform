"""Core teaching logic: stub airfoil generation and CST inverse."""

from typing import List
from airfoil_platform.contracts.common import Point2D
from airfoil_platform.core.geometry import generate_airfoil_2d

FIXED_CST_FOR_TEACHING = [0.1, 0.15, 0.12, 0.1, 0.08, 0.05, -0.1, -0.12, -0.1, -0.08, -0.05, -0.02]


def generate_teaching_airfoil() -> List[Point2D]:
    """Stub: ignore control points, always return fixed airfoil."""
    return generate_airfoil_2d(FIXED_CST_FOR_TEACHING)


def inverse_cst_from_airfoil(points: List[Point2D]) -> List[float]:
    """Stub: ignore input points, always return fixed CST params."""
    return list(FIXED_CST_FOR_TEACHING)
