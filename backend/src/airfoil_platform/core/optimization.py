from __future__ import annotations

from airfoil_platform.config.settings import (
    REAR_SPAR_WEB_THICKNESS_MAX,
    REAR_SPAR_WEB_THICKNESS_MIN,
    RIB_SPACING_MAX,
    RIB_SPACING_MIN,
    RIB_THICKNESS_MAX,
    RIB_THICKNESS_MIN,
)
from airfoil_platform.core.aerodynamics import compute_lift_drag_ratio
from airfoil_platform.core.structure import compute_weight


def optimize_cst(cst_params: list[float]) -> list[float]:
    return [round(cst_params[i] * (1.0 + 0.05 * (i + 1) / 12.0), 6) for i in range(12)]


def optimize_structure(
    rear_spar_web_thickness: float,
    rib_thickness: float,
    rib_spacing: float,
    target_reduction_ratio: float,
) -> tuple[float, float, float]:
    factor = 1.0 - target_reduction_ratio * 0.5
    new_rear = max(REAR_SPAR_WEB_THICKNESS_MIN, min(REAR_SPAR_WEB_THICKNESS_MAX,
                   round(rear_spar_web_thickness * factor, 6)))
    new_rib_t = max(RIB_THICKNESS_MIN, min(RIB_THICKNESS_MAX,
                    round(rib_thickness * factor, 6)))
    new_rib_s = max(RIB_SPACING_MIN, min(RIB_SPACING_MAX,
                    round(rib_spacing * (1.0 + target_reduction_ratio * 0.2), 6)))
    return new_rear, new_rib_t, new_rib_s


def compute_improvement_ratio(original_lift_drag: float, optimized_lift_drag: float) -> float:
    return round((optimized_lift_drag - original_lift_drag) / original_lift_drag, 6)


def compute_reduction_ratio(original_weight: float, optimized_weight: float) -> float:
    return round((original_weight - optimized_weight) / original_weight, 6)
