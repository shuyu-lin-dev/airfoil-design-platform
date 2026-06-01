from __future__ import annotations

from airfoil_platform.contracts.common import StructureDesign
from airfoil_platform.contracts.optimization import (
    AeroOptimizationRequest,
    AeroOptimizationResponse,
    CoupledOptimizationRequest,
    CoupledOptimizationResponse,
    StructOptimizationRequest,
    StructOptimizationResponse,
)
from airfoil_platform.core.aerodynamics import compute_lift_drag_ratio
from airfoil_platform.core.optimization import (
    compute_improvement_ratio,
    compute_reduction_ratio,
    optimize_cst,
    optimize_structure,
)
from airfoil_platform.core.structure import compute_weight


def optimize_aero(request: AeroOptimizationRequest) -> AeroOptimizationResponse:
    optimized_cst = optimize_cst(request.cst_params)
    orig_ld = compute_lift_drag_ratio(request.cst_params, request.condition.mach, request.condition.angle_of_attack)
    opt_ld = compute_lift_drag_ratio(optimized_cst, request.condition.mach, request.condition.angle_of_attack)
    return AeroOptimizationResponse(
        original=list(request.cst_params),
        optimized=optimized_cst,
        actual_improvement_ratio=compute_improvement_ratio(orig_ld, opt_ld),
    )


def optimize_struct(request: StructOptimizationRequest) -> StructOptimizationResponse:
    sd = request.structure_design
    new_rear, new_rib_t, new_rib_s = optimize_structure(
        sd.rear_spar_web_thickness, sd.rib_thickness, sd.rib_spacing,
        request.target_reduction_ratio,
    )
    wp = request.wing_planform
    mp = request.material_properties
    kw = {}
    if mp and mp.skin:
        kw["skin_density"] = mp.skin.material_density
    if mp and mp.internal_structure:
        kw["internal_density"] = mp.internal_structure.material_density

    orig_weight = compute_weight(
        request.cst_params, wp.span, wp.chord,
        sd.rear_spar_web_thickness, sd.rib_thickness, sd.rib_spacing, **kw,
    )
    opt_weight = compute_weight(
        request.cst_params, wp.span, wp.chord,
        new_rear, new_rib_t, new_rib_s, **kw,
    )
    optimized_sd = StructureDesign(
        rear_spar_web_thickness=new_rear,
        rib_thickness=new_rib_t,
        rib_spacing=new_rib_s,
    )
    return StructOptimizationResponse(
        original=sd,
        optimized=optimized_sd,
        actual_reduction_ratio=compute_reduction_ratio(orig_weight, opt_weight),
    )


def optimize_coupled(request: CoupledOptimizationRequest) -> CoupledOptimizationResponse:
    # Step 1: aerodynamic optimization
    optimized_cst = optimize_cst(request.cst_params)
    # Step 2: structural optimization
    sd = request.structure_design
    new_rear, new_rib_t, new_rib_s = optimize_structure(
        sd.rear_spar_web_thickness, sd.rib_thickness, sd.rib_spacing,
        request.target_improvement_ratio,
    )
    # Step 3: compute fitness (lift_drag_ratio / weight)
    wp = request.wing_planform
    mp = request.material_properties
    kw = {}
    if mp and mp.skin:
        kw["skin_density"] = mp.skin.material_density
    if mp and mp.internal_structure:
        kw["internal_density"] = mp.internal_structure.material_density

    orig_ld = compute_lift_drag_ratio(request.cst_params, request.condition.mach, request.condition.angle_of_attack)
    orig_w = compute_weight(request.cst_params, wp.span, wp.chord,
                            sd.rear_spar_web_thickness, sd.rib_thickness, sd.rib_spacing, **kw)
    opt_ld = compute_lift_drag_ratio(optimized_cst, request.condition.mach, request.condition.angle_of_attack)
    opt_w = compute_weight(optimized_cst, wp.span, wp.chord,
                           new_rear, new_rib_t, new_rib_s, **kw)
    orig_fitness = orig_ld / max(orig_w, 1e-12)
    opt_fitness = opt_ld / max(opt_w, 1e-12)

    return CoupledOptimizationResponse(
        original_cst=list(request.cst_params),
        optimized_cst=optimized_cst,
        original_structure=sd,
        optimized_structure=StructureDesign(
            rear_spar_web_thickness=new_rear,
            rib_thickness=new_rib_t,
            rib_spacing=new_rib_s,
        ),
        actual_improvement_ratio=compute_improvement_ratio(orig_fitness, opt_fitness),
    )
