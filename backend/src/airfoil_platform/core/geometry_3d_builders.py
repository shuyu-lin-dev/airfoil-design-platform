"""Core geometry logic: 3D wing CAD primitive builders and STEP reader."""

import math
from typing import List, Tuple

import numpy as np

from airfoil_platform.contracts.common import Point2D
from airfoil_platform.core.geometry_2d import (
    cst_class_function,
    cst_shape_function,
    generate_airfoil_2d,
)
from airfoil_platform.config import settings


def airfoil_points_scaled(cst_params: List[float], chord: float,
                          n_points: int = 200) -> List[Tuple[float, float]]:
    """Generate CST airfoil points scaled by chord."""
    pts = generate_airfoil_2d(cst_params, n_points)
    return [(p.x * chord, p.y * chord) for p in pts]


def compute_rib_positions(semi_span: float, rib_spacing: float) -> List[float]:
    """Compute rib z-positions. Returns list of z positions from root to tip."""
    rib_count = int(math.floor(semi_span / rib_spacing)) + 1
    if rib_count < 2:
        rib_count = 2
    actual_spacing = semi_span / (rib_count - 1)
    if actual_spacing > rib_spacing:
        rib_count += 1
        actual_spacing = semi_span / (rib_count - 1)
    return [i * actual_spacing for i in range(rib_count)]


def check_wingbox_thickness(cst_params: List[float], chord: float) -> bool:
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


# ---- CAD primitive builders ----


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
        nx = -dy / length
        ny = dx / length
        if pts[i][1] > 0:
            ny = -abs(ny) if ny > 0 else ny
        else:
            ny = abs(ny) if ny < 0 else ny
        sign = -1.0 if pts[i][1] >= 0 else 1.0
        result.append((
            pts[i][0] + sign * abs(nx) * distance,
            pts[i][1] + sign * abs(ny) * distance,
        ))
    return result


def _make_skin_solid(cq, profile_pts: list, semi_span: float, skin_t: float):
    """Create hollow skin solid: outer face extruded, then subtract offset inner."""
    pts_2d = _deduplicate([(p[0], p[1]) for p in profile_pts])

    outer_solid = (
        cq.Workplane("XY")
        .polyline(pts_2d)
        .close()
        .extrude(semi_span)
    )

    inner_pts = _offset_profile_inward(profile_pts, skin_t)
    inner_pts_2d = _deduplicate([(p[0], p[1]) for p in inner_pts])
    inner_solid = (
        cq.Workplane("XY")
        .polyline(inner_pts_2d)
        .close()
        .extrude(semi_span)
    )

    return outer_solid.cut(inner_solid)


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


def _make_spar(cq, profile_pts: list, semi_span: float, x_pos: float, thickness: float):
    """Create a spar as a rectangular plate at a given x position."""
    y_upper, y_lower = _profile_y_at_x(profile_pts, x_pos)
    half_t = thickness / 2.0

    spar = (
        cq.Workplane("XY")
        .transformed(offset=(x_pos - half_t, y_lower, 0))
        .box(thickness, y_upper - y_lower, semi_span, centered=False)
    )
    return spar


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
