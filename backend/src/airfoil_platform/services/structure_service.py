from __future__ import annotations

from airfoil_platform.contracts.structure import (
    StructurePredictionRequest,
    StructurePredictionResponse,
)
from airfoil_platform.core.structure import compute_max_stress, compute_weight


def predict(request: StructurePredictionRequest) -> StructurePredictionResponse:
    wp = request.wing_planform
    sd = request.structure_design
    mp = request.material_properties

    skin_dens = mp.skin.material_density if mp and mp.skin else None
    internal_dens = mp.internal_structure.material_density if mp and mp.internal_structure else None
    skin_e = mp.skin.elastic_modulus if mp and mp.skin else None
    internal_e = mp.internal_structure.elastic_modulus if mp and mp.internal_structure else None

    kw_weight = {}
    if skin_dens is not None:
        kw_weight["skin_density"] = skin_dens
    if internal_dens is not None:
        kw_weight["internal_density"] = internal_dens

    kw_stress = {}
    if skin_e is not None:
        kw_stress["skin_elastic_modulus"] = skin_e
    if internal_e is not None:
        kw_stress["internal_elastic_modulus"] = internal_e

    weight = compute_weight(
        cst_params=request.cst_params,
        span=wp.span, chord=wp.chord,
        rear_spar_web_thickness=sd.rear_spar_web_thickness,
        rib_thickness=sd.rib_thickness,
        rib_spacing=sd.rib_spacing,
        **kw_weight,
    )

    max_stress = compute_max_stress(
        cst_params=request.cst_params,
        span=wp.span, chord=wp.chord,
        mach=request.condition.mach,
        angle_of_attack_deg=request.condition.angle_of_attack,
        rear_spar_web_thickness=sd.rear_spar_web_thickness,
        rib_thickness=sd.rib_thickness,
        **kw_stress,
    )

    return StructurePredictionResponse(max_stress=max_stress, weight=weight)
