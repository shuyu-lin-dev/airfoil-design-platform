"""Core optimization logic: stub optimization algorithms."""

from typing import List

from airfoil_platform.config import settings
from airfoil_platform.core.aerodynamics import predict_lift_drag_ratio
from airfoil_platform.core.structure import predict_weight


def _perturb_cst_params(cst_params: List[float]) -> List[float]:
    """Stub: perturb each CST parameter proportionally."""
    return [c * (1.0 + 0.05 * (i + 1) / 12.0) for i, c in enumerate(cst_params)]


def _perturb_structure_params(rear_spar_web_thickness: float,
                              rib_thickness: float, rib_spacing: float):
    """Stub: reduce structure params by 3%, clamp to valid ranges."""
    opt_rear = max(settings.REAR_SPAR_WEB_THICKNESS_MIN,
                   min(settings.REAR_SPAR_WEB_THICKNESS_MAX,
                       rear_spar_web_thickness * 0.97))
    opt_rib_t = max(settings.RIB_THICKNESS_MIN,
                    min(settings.RIB_THICKNESS_MAX, rib_thickness * 0.97))
    opt_rib_s = max(settings.RIB_SPACING_MIN,
                    min(settings.RIB_SPACING_MAX, rib_spacing * 1.03))
    return opt_rear, opt_rib_t, opt_rib_s


def aerodynamic_optimize(
    cst_params: List[float], mach: float, aoa: float,
    target_improvement_ratio: float,
) -> dict:
    """Stub aerodynamic optimization. Returns optimized cst_params and metrics."""
    original_ld = predict_lift_drag_ratio(cst_params, mach, aoa)
    optimized_cst = _perturb_cst_params(cst_params)

    optimized_ld = original_ld * (1.0 + target_improvement_ratio)
    actual_improvement = ((optimized_ld - original_ld) / abs(original_ld)
                          if original_ld != 0 else 1.0)

    return {
        "original_lift_drag_ratio": original_ld,
        "optimized_cst_params": optimized_cst,
        "optimized_lift_drag_ratio": optimized_ld,
        "actual_improvement_ratio": actual_improvement,
    }


def structural_optimize(
    cst_params: List[float], span: float, chord: float,
    rear_spar_web_thickness: float, rib_thickness: float, rib_spacing: float,
    skin_material, internal_material, target_reduction_ratio: float,
) -> dict:
    """Stub structural optimization. Returns optimized structure params and weight."""
    original_weight = predict_weight(
        cst_params, span, chord,
        rear_spar_web_thickness, rib_thickness, rib_spacing,
        skin_material, internal_material,
    )

    opt_rear, opt_rib_t, opt_rib_s = _perturb_structure_params(
        rear_spar_web_thickness, rib_thickness, rib_spacing)

    optimized_weight = predict_weight(
        cst_params, span, chord, opt_rear, opt_rib_t, opt_rib_s,
        skin_material, internal_material,
    )

    actual_reduction = ((original_weight - optimized_weight) / original_weight
                        if original_weight > 0 else 0.0)

    return {
        "original_weight": original_weight,
        "optimized_rear_spar_web_thickness": opt_rear,
        "optimized_rib_thickness": opt_rib_t,
        "optimized_rib_spacing": opt_rib_s,
        "optimized_weight": optimized_weight,
        "actual_reduction_ratio": actual_reduction,
    }


def coupled_optimize(
    cst_params: List[float], mach: float, aoa: float,
    span: float, chord: float,
    rear_spar_web_thickness: float, rib_thickness: float, rib_spacing: float,
    skin_material, internal_material, target_improvement_ratio: float,
) -> dict:
    """Stub coupled optimization. Returns optimized params and fitness metrics."""
    original_ld = predict_lift_drag_ratio(cst_params, mach, aoa)
    original_weight = predict_weight(
        cst_params, span, chord,
        rear_spar_web_thickness, rib_thickness, rib_spacing,
        skin_material, internal_material,
    )
    original_fitness = original_ld / original_weight if original_weight > 0 else 0.0

    optimized_cst = _perturb_cst_params(cst_params)
    opt_rear, opt_rib_t, opt_rib_s = _perturb_structure_params(
        rear_spar_web_thickness, rib_thickness, rib_spacing)

    optimized_ld = original_ld * (1.0 + target_improvement_ratio * 0.6)
    optimized_weight = predict_weight(
        optimized_cst, span, chord, opt_rear, opt_rib_t, opt_rib_s,
        skin_material, internal_material,
    )
    optimized_fitness = optimized_ld / optimized_weight if optimized_weight > 0 else 0.0

    actual_improvement = ((optimized_fitness - original_fitness) / abs(original_fitness)
                          if original_fitness != 0 else 1.0)

    return {
        "original_weight": original_weight,
        "original_lift_drag_ratio": original_ld,
        "original_fitness": original_fitness,
        "optimized_cst_params": optimized_cst,
        "optimized_rear_spar_web_thickness": opt_rear,
        "optimized_rib_thickness": opt_rib_t,
        "optimized_rib_spacing": opt_rib_s,
        "optimized_weight": optimized_weight,
        "optimized_lift_drag_ratio": optimized_ld,
        "optimized_fitness": optimized_fitness,
        "actual_improvement_ratio": actual_improvement,
    }
