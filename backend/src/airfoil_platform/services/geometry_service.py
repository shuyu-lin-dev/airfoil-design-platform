"""Geometry service: orchestrates airfoil/wing generation workflows."""

from airfoil_platform.lib.ids import generate_artifact_id
from airfoil_platform.artifacts.step_store import write_step_artifact
from airfoil_platform.artifacts.artifact_registry import read_sidecar
from airfoil_platform.contracts.geometry import (
    Airfoil2DResponse,
    Wing3DResponse,
    GeometryArtifactMeta,
)
from airfoil_platform.core.geometry import generate_airfoil_2d, generate_wing_3d_step


def generate_airfoil_2d_service(cst_params: list) -> Airfoil2DResponse:
    points = generate_airfoil_2d(cst_params)
    return Airfoil2DResponse(points=points)


def generate_wing_3d_service(
    cst_params: list,
    span: float,
    chord: float,
    rear_spar_web_thickness: float,
    rib_thickness: float,
    rib_spacing: float,
) -> Wing3DResponse:
    artifact_id = generate_artifact_id({
        "cst_params": cst_params,
        "span": span,
        "chord": chord,
        "rear_spar_web_thickness": rear_spar_web_thickness,
        "rib_thickness": rib_thickness,
        "rib_spacing": rib_spacing,
    })

    step_bytes = generate_wing_3d_step(
        cst_params=cst_params,
        chord=chord,
        span=span,
        rear_spar_web_thickness=rear_spar_web_thickness,
        rib_thickness=rib_thickness,
        rib_spacing=rib_spacing,
    )

    write_step_artifact(
        artifact_id=artifact_id,
        step_content=step_bytes,
        components=["skin", "front_spar", "rear_spar", "ribs"],
    )

    meta = read_sidecar("geometry", artifact_id)
    geom_artifact = GeometryArtifactMeta(**meta)
    return Wing3DResponse(geometry_artifact=geom_artifact)
