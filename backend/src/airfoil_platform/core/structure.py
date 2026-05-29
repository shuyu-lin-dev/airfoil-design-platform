"""Core structure logic: stub weight and stress predictions."""

import math
from typing import List

from airfoil_platform.contracts.common import MaterialGroup
from airfoil_platform.core.geometry import cst_class_function, cst_shape_function
from airfoil_platform.config import settings


def _airfoil_thickness_at(cst_params: List[float], x_norm: float) -> float:
    """Return upper - lower y at normalized x position."""
    upper = cst_params[:6]
    lower = cst_params[6:]
    c = cst_class_function(x_norm)
    y_upper = c * cst_shape_function(upper, x_norm)
    y_lower = c * cst_shape_function(lower, x_norm)
    return y_upper - y_lower


def _airfoil_area(cst_params: List[float], n_samples: int = 100) -> float:
    """Approximate airfoil cross-sectional area using trapezoidal rule."""
    area = 0.0
    dx = 1.0 / n_samples
    for i in range(n_samples):
        x0 = i * dx
        x1 = (i + 1) * dx
        t0 = _airfoil_thickness_at(cst_params, x0)
        t1 = _airfoil_thickness_at(cst_params, x1)
        area += (t0 + t1) / 2.0 * dx
    return area


def predict_weight(
    cst_params: List[float],
    span: float,
    chord: float,
    rear_spar_web_thickness: float,
    rib_thickness: float,
    rib_spacing: float,
    skin_material: MaterialGroup,
    internal_material: MaterialGroup,
) -> float:
    """Compute structural weight (N) from geometry and materials."""
    semi_span = span / 2.0
    skin_t = settings.SKIN_THICKNESS
    front_spar_t = rear_spar_web_thickness * settings.FRONT_SPAR_WEB_THICKNESS_RATIO

    # Skin volume (upper + lower surfaces, both sides of right semi-wing)
    skin_volume = chord * semi_span * skin_t * 2.0

    # Spar volumes
    t_front = _airfoil_thickness_at(cst_params, settings.FRONT_SPAR_CHORD_FRACTION) * chord
    t_rear = _airfoil_thickness_at(cst_params, settings.REAR_SPAR_CHORD_FRACTION) * chord
    front_spar_volume = max(t_front, 0.0) * semi_span * front_spar_t
    rear_spar_volume = max(t_rear, 0.0) * semi_span * rear_spar_web_thickness

    # Rib volume
    airfoil_area = _airfoil_area(cst_params) * chord * chord
    rib_count = int(math.floor(semi_span / rib_spacing)) + 1
    if semi_span / (rib_count - 1) > rib_spacing:
        rib_count += 1
    ribs_volume = airfoil_area * rib_thickness * rib_count

    # Masses (right semi-wing)
    skin_mass = skin_volume * skin_material.material_density
    internal_mass = (front_spar_volume + rear_spar_volume + ribs_volume) * \
                    internal_material.material_density

    # Full wing weight (2x for left side)
    full_mass = (skin_mass + internal_mass) * 2.0
    return full_mass * settings.G


def predict_max_stress() -> float:
    """Stub maximum equivalent stress (Pa)."""
    return 250_000_000.0  # 250 MPa, typical aluminum alloy stress
