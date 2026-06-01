from __future__ import annotations

import json
from pathlib import Path

from airfoil_platform.artifacts import generate_artifact_id
from airfoil_platform.config.settings import ARTIFACT_ROOT
from airfoil_platform.contracts.artifacts import ArtifactMetadataResponse
from airfoil_platform.contracts.geometry import (
    Airfoil2DRequest,
    Airfoil2DResponse,
    AirfoilPoint,
    Wing3DRequest,
    Wing3DResponse,
)
from airfoil_platform.core.geometry import build_wing_3d, cst_to_airfoil_points


def generate_airfoil_2d(request: Airfoil2DRequest) -> Airfoil2DResponse:
    upper, lower = cst_to_airfoil_points(request.cst_params, n_points=100)
    points = [AirfoilPoint(x=pt[0], y=pt[1]) for pt in upper] + [
        AirfoilPoint(x=pt[0], y=pt[1]) for pt in lower
    ]
    return Airfoil2DResponse(points=points)


def _save_assembly_and_sidecar(assy, artifact_id, component_names, artifact_root):
    role_dir = Path(artifact_root) / "geometry"
    role_dir.mkdir(parents=True, exist_ok=True)
    step_path = role_dir / f"{artifact_id}.step"
    assy.save(str(step_path))
    sidecar = {
        "artifact_id": artifact_id,
        "format": "step",
        "role": "structural_step",
        "path": str(step_path),
        "status": "ready",
        "components": component_names,
    }
    sidecar_path = role_dir / f"{artifact_id}.json"
    sidecar_path.write_text(json.dumps(sidecar, indent=2))
    return sidecar


def generate_wing_3d(request: Wing3DRequest, artifact_root: str = ARTIFACT_ROOT) -> Wing3DResponse:
    wp = request.wing_planform
    sd = request.structure_design

    assy = build_wing_3d(
        cst_params=request.cst_params,
        span=wp.span,
        chord=wp.chord,
        rear_spar_web_thickness=sd.rear_spar_web_thickness,
        rib_thickness=sd.rib_thickness,
        rib_spacing=sd.rib_spacing,
    )

    input_params = {
        "cst_params": request.cst_params,
        "span": wp.span, "chord": wp.chord,
        "rear_spar_web_thickness": sd.rear_spar_web_thickness,
        "rib_thickness": sd.rib_thickness,
        "rib_spacing": sd.rib_spacing,
    }
    artifact_id = generate_artifact_id(input_params)
    component_names = [child.name for child in assy.children if child.name is not None]
    sidecar = _save_assembly_and_sidecar(assy, artifact_id, component_names, artifact_root)

    ga = ArtifactMetadataResponse(
        artifact_id=sidecar["artifact_id"],
        format=sidecar["format"],
        role=sidecar["role"],
        path=sidecar["path"],
        status=sidecar["status"],
        components=sidecar["components"],
    )
    return Wing3DResponse(geometry_artifact=ga)
