from __future__ import annotations

from airfoil_platform.artifacts import generate_artifact_id, write_hdf5_artifact
from airfoil_platform.config.settings import ARTIFACT_ROOT
from airfoil_platform.contracts.aerodynamics import (
    AerodynamicPredictionRequest,
    AerodynamicPredictionResponse,
)
from airfoil_platform.contracts.artifacts import ArtifactMetadataResponse
from airfoil_platform.contracts.geometry import AirfoilPoint
from airfoil_platform.core.aerodynamics import (
    compute_cp_distribution,
    compute_lift_drag_ratio,
    generate_field_data,
)
from airfoil_platform.core.geometry import cst_to_airfoil_points


def predict(request: AerodynamicPredictionRequest, artifact_root: str = ARTIFACT_ROOT) -> AerodynamicPredictionResponse:
    upper, lower = cst_to_airfoil_points(request.cst_params, n_points=100)
    points = [AirfoilPoint(x=pt[0], y=pt[1]) for pt in upper] + [
        AirfoilPoint(x=pt[0], y=pt[1]) for pt in lower
    ]

    lift_drag = compute_lift_drag_ratio(
        request.cst_params, request.condition.mach, request.condition.angle_of_attack
    )
    cp = compute_cp_distribution(
        points, request.condition.mach, request.condition.angle_of_attack
    )
    coords, pressure, velocity = generate_field_data(
        points, request.condition.mach, request.condition.angle_of_attack
    )

    input_params = {
        "cst_params": request.cst_params,
        "mach": request.condition.mach,
        "aoa": request.condition.angle_of_attack,
    }
    artifact_id = generate_artifact_id(input_params)
    sidecar = write_hdf5_artifact(artifact_id, coords, pressure, velocity, artifact_root)

    field_artifact = ArtifactMetadataResponse(
        artifact_id=sidecar["artifact_id"],
        format=sidecar["format"],
        role=sidecar["role"],
        path=sidecar["path"],
        status=sidecar["status"],
        datasets=sidecar["datasets"],
    )

    return AerodynamicPredictionResponse(
        lift_drag_ratio=round(lift_drag, 4),
        cp_distribution=cp,
        field_artifact=field_artifact,
    )
