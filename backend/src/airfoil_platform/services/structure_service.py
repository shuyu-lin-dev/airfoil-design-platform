"""Structure prediction service."""

from airfoil_platform.contracts.structure import StructurePredictResponse
from airfoil_platform.core.structure import predict_weight, predict_max_stress


def predict_structure_service(
    cst_params: list,
    span: float,
    chord: float,
    rear_spar_web_thickness: float,
    rib_thickness: float,
    rib_spacing: float,
    skin_material,
    internal_material,
) -> StructurePredictResponse:
    weight = predict_weight(
        cst_params=cst_params,
        span=span,
        chord=chord,
        rear_spar_web_thickness=rear_spar_web_thickness,
        rib_thickness=rib_thickness,
        rib_spacing=rib_spacing,
        skin_material=skin_material,
        internal_material=internal_material,
    )
    max_stress = predict_max_stress()
    return StructurePredictResponse(max_stress=max_stress, weight=weight)
