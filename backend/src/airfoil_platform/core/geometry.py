"""Core geometry logic — re-exports from geometry_2d, geometry_3d, geometry_3d_builders."""

from airfoil_platform.core.geometry_2d import (
    cst_class_function,
    bernstein_polynomial,
    cst_shape_function,
    generate_airfoil_2d,
)
from airfoil_platform.core.geometry_3d import generate_wing_3d_step, read_step_components
from airfoil_platform.core.geometry_3d_builders import (
    airfoil_points_scaled,
    check_wingbox_thickness,
    compute_rib_positions,
)

__all__ = [
    "cst_class_function",
    "bernstein_polynomial",
    "cst_shape_function",
    "generate_airfoil_2d",
    "generate_wing_3d_step",
    "airfoil_points_scaled",
    "check_wingbox_thickness",
    "compute_rib_positions",
    "read_step_components",
]
