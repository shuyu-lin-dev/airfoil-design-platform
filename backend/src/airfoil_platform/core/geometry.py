"""Core geometry logic: CST airfoil generation and 3D wing CAD."""

import math
import os
import tempfile
import shutil
from typing import List, Tuple
import numpy as np
from airfoil_platform.contracts.common import Point2D
from airfoil_platform.config import settings


def cst_class_function(x: float, n1: float = 0.5, n2: float = 1.0) -> float:
    return (x ** n1) * ((1.0 - x) ** n2)


def bernstein_polynomial(i: int, n: int, x: float) -> float:
    if i < 0 or i > n:
        return 0.0
    coeff = math.comb(n, i)
    return coeff * (x ** i) * ((1.0 - x) ** (n - i))


def cst_shape_function(coeffs: List[float], x: float) -> float:
    n = len(coeffs) - 1
    s = 0.0
    for i, c in enumerate(coeffs):
        s += c * bernstein_polynomial(i, n, x)
    return s


def generate_airfoil_2d(cst_params: List[float], n_points: int = 200) -> List[Point2D]:
    """
    Generate 2D airfoil points using CST parameterization.
    cst_params: 12 values — first 6 upper surface, last 6 lower surface.
    Returns 200 points: first 100 upper (LE to TE), last 100 lower (TE to LE).
    """
    upper_coeffs = cst_params[:6]
    lower_coeffs = cst_params[6:]

    half_n = n_points // 2  # 100

    points: List[Point2D] = []

    # Upper surface: LE (x=0) to TE (x=1)
    for i in range(half_n):
        x = 1.0 - (math.cos(math.pi * i / (half_n - 1)) + 1.0) / 2.0 if half_n > 1 else 1.0
        c = cst_class_function(x)
        s_upper = cst_shape_function(upper_coeffs, x)
        y = c * s_upper
        points.append(Point2D(x=x, y=y))

    # Lower surface: TE (x=1) to LE (x=0)
    for i in range(half_n):
        x = (math.cos(math.pi * i / (half_n - 1)) + 1.0) / 2.0 if half_n > 1 else 0.0
        c = cst_class_function(x)
        s_lower = cst_shape_function(lower_coeffs, x)
        y = c * s_lower
        points.append(Point2D(x=x, y=y))

    return points


# ---- 3D Wing CAD Generation ----

def _airfoil_points_scaled(cst_params: List[float], chord: float,
                            n_points: int = 200) -> List[Tuple[float, float]]:
    """Generate CST airfoil points scaled by chord."""
    pts = generate_airfoil_2d(cst_params, n_points)
    return [(p.x * chord, p.y * chord) for p in pts]


def _check_wingbox_thickness(cst_params: List[float], chord: float) -> bool:
    """Check if wing box section thickness >= 2 * skin_thickness at every station."""
    upper = cst_params[:6]
    lower = cst_params[6:]
    skin_t = settings.SKIN_THICKNESS
    fspar = settings.FRONT_SPAR_CHORD_FRACTION
    rspar = settings.REAR_SPAR_CHORD_FRACTION

    for x_norm in np.linspace(fspar, rspar, 20):
        c = cst_class_function(x_norm)
        s_upper = cst_shape_function(upper, x_norm)
        s_lower = cst_shape_function(lower, x_norm)
        y_upper = c * s_upper * chord
        y_lower = c * s_lower * chord
        thickness = y_upper - y_lower
        if thickness < 2.0 * skin_t:
            return False
    return True


def _compute_rib_positions(semi_span: float, rib_spacing: float) -> List[float]:
    """Compute rib z-positions. Returns list of z positions from root to tip."""
    rib_count = int(math.floor(semi_span / rib_spacing)) + 1
    if rib_count < 2:
        rib_count = 2
    # Check if last rib reaches tip
    actual_spacing = semi_span / (rib_count - 1)
    if actual_spacing > rib_spacing:
        rib_count += 1
        actual_spacing = semi_span / (rib_count - 1)
    return [i * actual_spacing for i in range(rib_count)]


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

    if not _check_wingbox_thickness(cst_params, chord):
        raise ValueError(
            "Wing box section thickness is insufficient for skin offset. "
            "At least one chord station in the wing box has thickness < 2 * skin_thickness."
        )

    # Generate airfoil profile
    profile_pts = _airfoil_points_scaled(cst_params, chord)
    rib_positions = _compute_rib_positions(semi_span, rib_spacing)

    # --- Skin solid ---
    skin_solid = _make_skin_solid(cq, profile_pts, semi_span, skin_t)

    # --- Spars ---
    front_spar = _make_spar(cq, profile_pts, semi_span, fspar_frac * chord, front_spar_t)
    rear_spar = _make_spar(cq, profile_pts, semi_span, rspar_frac * chord, rear_spar_web_thickness)

    # --- Ribs ---
    rib_solids = []
    for z in rib_positions:
        rib = _make_rib(cq, profile_pts, z, rib_thickness)
        rib_solids.append(rib)
    ribs_compound = _union_solids(rib_solids)

    # --- Assembly ---
    assembly = cq.Assembly()
    assembly.add(skin_solid, name="skin")
    assembly.add(front_spar, name="front_spar")
    assembly.add(rear_spar, name="rear_spar")
    assembly.add(ribs_compound, name="ribs")

    # Export STEP
    tmp_dir = tempfile.mkdtemp()
    tmp_step = os.path.join(tmp_dir, "wing.step")
    try:
        assembly.save(tmp_step)
        with open(tmp_step, "rb") as f:
            return f.read()
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _make_skin_solid(cq, profile_pts: list, semi_span: float, skin_t: float):
    """Create hollow skin solid: outer face extruded, then subtract offset inner."""
    pts_2d = _deduplicate([(p[0], p[1]) for p in profile_pts])

    # Outer solid
    outer_solid = (
        cq.Workplane("XY")
        .polyline(pts_2d)
        .close()
        .extrude(semi_span)
    )

    # Offset inner profile inward
    inner_pts = _offset_profile_inward(profile_pts, skin_t)
    inner_pts_2d = _deduplicate([(p[0], p[1]) for p in inner_pts])
    inner_solid = (
        cq.Workplane("XY")
        .polyline(inner_pts_2d)
        .close()
        .extrude(semi_span)
    )

    skin = outer_solid.cut(inner_solid)
    return skin


def _deduplicate(pts_2d: list, tol: float = 1e-8) -> list:
    """Remove consecutive points that are too close (for CadQuery polyline)."""
    if len(pts_2d) < 2:
        return pts_2d
    result = [pts_2d[0]]
    for pt in pts_2d[1:]:
        last = result[-1]
        dx = pt[0] - last[0]
        dy = pt[1] - last[1]
        if dx * dx + dy * dy > tol * tol:
            result.append(pt)
    # Also check last-to-first wrap
    dx = result[-1][0] - result[0][0]
    dy = result[-1][1] - result[0][1]
    if dx * dx + dy * dy <= tol * tol:
        result.pop()
    return result


def _offset_profile_inward(profile_pts: list, distance: float) -> list:
    """Offset a closed profile inward by a fixed distance using local normals."""
    pts = [(p[0], p[1]) for p in profile_pts]
    n = len(pts)
    result = []
    for i in range(n):
        prev_pt = pts[(i - 1) % n]
        next_pt = pts[(i + 1) % n]
        dx = next_pt[0] - prev_pt[0]
        dy = next_pt[1] - prev_pt[1]
        length = math.sqrt(dx * dx + dy * dy)
        if length < 1e-12:
            result.append(pts[i])
            continue
        # Normal pointing inward (rotate tangent 90° CW for upper, CCW for lower)
        nx = -dy / length
        ny = dx / length
        # Determine direction: for upper surface (y > 0), inward is downward
        if pts[i][1] > 0:
            ny = -abs(ny) if ny > 0 else ny
        else:
            ny = abs(ny) if ny < 0 else ny
        # Use signed distance based on position
        # Upper surface points have positive y, inner direction is -y
        # Lower surface points have negative y, inner direction is +y
        sign = -1.0 if pts[i][1] >= 0 else 1.0
        result.append((
            pts[i][0] + sign * abs(nx) * distance,
            pts[i][1] + sign * abs(ny) * distance,
        ))
    return result


def _make_spar(cq, profile_pts: list, semi_span: float, x_pos: float, thickness: float):
    """Create a spar as a rectangular plate at a given x position."""
    # Find upper and lower y at this x position
    y_upper, y_lower = _profile_y_at_x(profile_pts, x_pos)
    half_t = thickness / 2.0

    spar = (
        cq.Workplane("XY")
        .transformed(offset=(x_pos - half_t, y_lower, 0))
        .box(thickness, y_upper - y_lower, semi_span, centered=False)
    )
    return spar


def _profile_y_at_x(profile_pts: list, x_target: float) -> Tuple[float, float]:
    """Find upper and lower surface y values at given x position."""
    upper_y = None
    lower_y = None
    for p in profile_pts:
        if abs(p[0] - x_target) < 0.01:
            y = p[1]
            if upper_y is None or y > upper_y:
                upper_y = y
            if lower_y is None or y < lower_y:
                lower_y = y

    if upper_y is None:
        # Interpolate
        upper_pts = [(p[0], p[1]) for p in profile_pts if p[1] >= 0]
        lower_pts = [(p[0], p[1]) for p in profile_pts if p[1] <= 0]
        upper_y = _interp_y(upper_pts, x_target)
        lower_y = _interp_y(lower_pts, x_target)
    return upper_y, lower_y


def _interp_y(pts: list, x_target: float) -> float:
    """Linear interpolation of y at x_target."""
    sorted_pts = sorted(pts, key=lambda p: p[0])
    for i in range(len(sorted_pts) - 1):
        x0, y0 = sorted_pts[i]
        x1, y1 = sorted_pts[i + 1]
        if x0 <= x_target <= x1:
            if abs(x1 - x0) < 1e-12:
                return (y0 + y1) / 2.0
            t = (x_target - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return sorted_pts[-1][1]


def _make_rib(cq, profile_pts: list, z_pos: float, thickness: float):
    """Create a rib as a thin extruded section at a given z position."""
    half_t = thickness / 2.0
    pts_2d = _deduplicate([(p[0], p[1]) for p in profile_pts])
    rib = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z_pos - half_t))
        .polyline(pts_2d)
        .close()
        .extrude(thickness)
    )
    return rib


def _union_solids(solids: list):
    """Union a list of solids into a single compound."""
    if len(solids) == 0:
        return None
    result = solids[0]
    for s in solids[1:]:
        result = result.union(s)
    return result


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
