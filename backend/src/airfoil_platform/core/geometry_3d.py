"""Core geometry logic: 3D wing STEP generation orchestration and reader."""

import os
import tempfile
import shutil
from typing import List, Tuple

from airfoil_platform.config import settings
from airfoil_platform.core.geometry_3d_builders import (
    airfoil_points_scaled,
    check_wingbox_thickness,
    compute_rib_positions,
    _make_skin_solid,
    _make_spar,
    _make_rib,
    _union_solids,
)


def _export_assembly_step(assembly, tmp_dir, step_path):
    """Export an Assembly to STEP and read back bytes."""
    import cadquery as cq
    assembly.save(step_path)
    with open(step_path, "rb") as f:
        return f.read()


def generate_wing_3d_step(
    cst_params: List[float],
    chord: float,
    span: float,
    rear_spar_web_thickness: float,
    rib_thickness: float,
    rib_spacing: float,
) -> bytes:
    """
    Generate a 3D wing structural STEP assembly using CadQuery.
    Returns STEP file content as bytes.
    Raises ValueError if wing box section is too thin.
    """
    import cadquery as cq

    semi_span = span / 2.0
    skin_t = settings.SKIN_THICKNESS
    fspar_frac = settings.FRONT_SPAR_CHORD_FRACTION
    rspar_frac = settings.REAR_SPAR_CHORD_FRACTION
    front_spar_t = rear_spar_web_thickness * settings.FRONT_SPAR_WEB_THICKNESS_RATIO

    if not check_wingbox_thickness(cst_params, chord):
        raise ValueError(
            "Wing box section thickness is insufficient for skin offset. "
            "At least one chord station in the wing box has thickness < 2 * skin_thickness."
        )

    profile_pts = airfoil_points_scaled(cst_params, chord)
    rib_positions = compute_rib_positions(semi_span, rib_spacing)

    skin_solid = _make_skin_solid(cq, profile_pts, semi_span, skin_t)
    front_spar = _make_spar(cq, profile_pts, semi_span, fspar_frac * chord, front_spar_t)
    rear_spar = _make_spar(cq, profile_pts, semi_span, rspar_frac * chord, rear_spar_web_thickness)

    rib_solids = [_make_rib(cq, profile_pts, z, rib_thickness) for z in rib_positions]
    ribs_compound = _union_solids(rib_solids)

    assembly = cq.Assembly()
    assembly.add(skin_solid, name="skin")
    assembly.add(front_spar, name="front_spar")
    assembly.add(rear_spar, name="rear_spar")
    assembly.add(ribs_compound, name="ribs")

    tmp_dir = tempfile.mkdtemp()
    tmp_step = os.path.join(tmp_dir, "wing.step")
    try:
        return _export_assembly_step(assembly, tmp_dir, tmp_step)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def read_step_components(file_path: str) -> Tuple[list, dict]:
    """
    Read a STEP file and return component names and bounding box info.
    Returns (components, bbox) where bbox has x_range, y_range, z_range.
    """
    import cadquery as cq

    result = cq.importers.importStep(file_path)
    shapes = []
    if hasattr(result, "vals"):
        shapes = list(result.vals())
    elif hasattr(result, "Solids"):
        shapes = list(result.Solids())
    else:
        shapes = [result] if result is not None else []

    bbox = {}
    for s in shapes:
        if s is None:
            continue
        bb = s.BoundingBox()
        xmin, xmax = bb.xmin, bb.xmax
        ymin, ymax = bb.ymin, bb.ymax
        zmin, zmax = bb.zmin, bb.zmax
        if not bbox:
            bbox = {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax,
                    "zmin": zmin, "zmax": zmax}
        else:
            bbox["xmin"] = min(bbox["xmin"], xmin)
            bbox["xmax"] = max(bbox["xmax"], xmax)
            bbox["ymin"] = min(bbox["ymin"], ymin)
            bbox["ymax"] = max(bbox["ymax"], ymax)
            bbox["zmin"] = min(bbox["zmin"], zmin)
            bbox["zmax"] = max(bbox["zmax"], zmax)

    return shapes, bbox
