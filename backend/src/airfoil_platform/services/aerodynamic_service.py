"""Aerodynamic prediction service: orchestrates prediction + artifact storage."""

from airfoil_platform.lib.ids import generate_artifact_id
from airfoil_platform.artifacts.hdf5_store import write_hdf5_artifact
from airfoil_platform.artifacts.artifact_registry import read_sidecar
from airfoil_platform.contracts.aerodynamics import (
    AerodynamicPredictResponse,
    FieldArtifactMeta,
)
from airfoil_platform.core.aerodynamics import (
    predict_lift_drag_ratio,
    predict_cp_distribution,
    generate_field_data,
)


def predict_aerodynamic_service(cst_params: list, mach: float, angle_of_attack: float
                                ) -> AerodynamicPredictResponse:
    lift_drag_ratio = predict_lift_drag_ratio(cst_params, mach, angle_of_attack)
    cp_distribution = predict_cp_distribution(cst_params)

    artifact_id = generate_artifact_id({
        "cst_params": cst_params,
        "mach": mach,
        "angle_of_attack": angle_of_attack,
    })
    coords, pressure, velocity = generate_field_data()
    write_hdf5_artifact(artifact_id, coords, pressure, velocity)

    meta = read_sidecar("aerodynamic", artifact_id)
    field_artifact = FieldArtifactMeta(**meta)

    return AerodynamicPredictResponse(
        lift_drag_ratio=lift_drag_ratio,
        cp_distribution=cp_distribution,
        field_artifact=field_artifact,
    )
