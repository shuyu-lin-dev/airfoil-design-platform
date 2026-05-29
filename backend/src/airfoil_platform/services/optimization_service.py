"""Optimization service: orchestrates optimization workflows."""

from airfoil_platform.contracts.common import Condition, WingPlanform, StructureDesign, MaterialProperties
from airfoil_platform.contracts.optimization import (
    AeroOptResponse, AeroOptOriginal, AeroOptOptimized,
    StructOptResponse, StructOptOriginal, StructOptOptimized,
    CoupledOptResponse, CoupledOptOriginal, CoupledOptOptimized,
)
from airfoil_platform.core.optimization import aerodynamic_optimize, structural_optimize, coupled_optimize


def aerodynamic_optimization_service(
    cst_params: list, mach: float, aoa: float, target: float,
) -> AeroOptResponse:
    result = aerodynamic_optimize(cst_params, mach, aoa, target)
    return AeroOptResponse(
        original=AeroOptOriginal(
            cst_params=cst_params,
            condition=Condition(mach=mach, angle_of_attack=aoa),
            lift_drag_ratio=result["original_lift_drag_ratio"],
        ),
        optimized=AeroOptOptimized(
            cst_params=result["optimized_cst_params"],
            condition=Condition(mach=mach, angle_of_attack=aoa),
            lift_drag_ratio=result["optimized_lift_drag_ratio"],
        ),
        actual_improvement_ratio=result["actual_improvement_ratio"],
    )


def structural_optimization_service(
    cst_params: list, mach: float, aoa: float, span: float, chord: float,
    rear_spar: float, rib_t: float, rib_s: float,
    skin_mat, internal_mat, target: float,
) -> StructOptResponse:
    result = structural_optimize(
        cst_params, span, chord, rear_spar, rib_t, rib_s,
        skin_mat, internal_mat, target,
    )
    orig_sd = StructureDesign(
        rear_spar_web_thickness=rear_spar, rib_thickness=rib_t, rib_spacing=rib_s,
    )
    opt_sd = StructureDesign(
        rear_spar_web_thickness=result["optimized_rear_spar_web_thickness"],
        rib_thickness=result["optimized_rib_thickness"],
        rib_spacing=result["optimized_rib_spacing"],
    )
    wp = WingPlanform(span=span, chord=chord)
    cond = Condition(mach=mach, angle_of_attack=aoa)
    # MaterialProperties with the specific materials used
    from airfoil_platform.contracts.common import MaterialGroup
    mp = MaterialProperties(skin=skin_mat, internal_structure=internal_mat)

    return StructOptResponse(
        original=StructOptOriginal(
            cst_params=cst_params, condition=cond, wing_planform=wp,
            structure_design=orig_sd, material_properties=mp,
            weight=result["original_weight"],
        ),
        optimized=StructOptOptimized(
            cst_params=cst_params, condition=cond, wing_planform=wp,
            structure_design=opt_sd, material_properties=mp,
            weight=result["optimized_weight"],
        ),
        actual_reduction_ratio=result["actual_reduction_ratio"],
    )


def coupled_optimization_service(
    cst_params: list, mach: float, aoa: float, span: float, chord: float,
    rear_spar: float, rib_t: float, rib_s: float,
    skin_mat, internal_mat, target: float,
) -> CoupledOptResponse:
    result = coupled_optimize(
        cst_params, mach, aoa, span, chord, rear_spar, rib_t, rib_s,
        skin_mat, internal_mat, target,
    )
    wp = WingPlanform(span=span, chord=chord)
    cond = Condition(mach=mach, angle_of_attack=aoa)
    from airfoil_platform.contracts.common import MaterialGroup
    mp = MaterialProperties(skin=skin_mat, internal_structure=internal_mat)

    orig_sd = StructureDesign(
        rear_spar_web_thickness=rear_spar, rib_thickness=rib_t, rib_spacing=rib_s,
    )
    opt_sd = StructureDesign(
        rear_spar_web_thickness=result["optimized_rear_spar_web_thickness"],
        rib_thickness=result["optimized_rib_thickness"],
        rib_spacing=result["optimized_rib_spacing"],
    )

    return CoupledOptResponse(
        original=CoupledOptOriginal(
            cst_params=cst_params, condition=cond, wing_planform=wp,
            structure_design=orig_sd, material_properties=mp,
            weight=result["original_weight"],
            lift_drag_ratio=result["original_lift_drag_ratio"],
            fitness=result["original_fitness"],
        ),
        optimized=CoupledOptOptimized(
            cst_params=result["optimized_cst_params"], condition=cond, wing_planform=wp,
            structure_design=opt_sd, material_properties=mp,
            weight=result["optimized_weight"],
            lift_drag_ratio=result["optimized_lift_drag_ratio"],
            fitness=result["optimized_fitness"],
        ),
        actual_improvement_ratio=result["actual_improvement_ratio"],
    )
