from __future__ import annotations

import math
from typing import Optional


def _berstein(i: int, n: int, psi: float) -> float:
    """Bernstein basis polynomial B_{i,n}(psi) = C(n,i) * psi^i * (1-psi)^{n-i}."""
    coeff = math.comb(n, i)
    return coeff * (psi ** i) * ((1.0 - psi) ** (n - i))


def _shape_function(coeffs: list[float], psi: float) -> float:
    """Evaluate the CST shape function S(psi) = sum A_i * B_i^n(psi)."""
    n = len(coeffs) - 1
    total = 0.0
    for i, a in enumerate(coeffs):
        total += a * _berstein(i, n, psi)
    return total


def _class_function(psi: float, n1: float = 0.5, n2: float = 1.0) -> float:
    """CST class function C(psi) = psi^n1 * (1-psi)^n2."""
    return (psi ** n1) * ((1.0 - psi) ** n2)


def _cosine_spacing(n: int) -> list[float]:
    """Generate n cosine-distributed points from 0 to 1."""
    return [(1.0 - math.cos(i * math.pi / (n - 1))) / 2.0 for i in range(n)]


def cst_to_airfoil_points(
    cst_params: list[float], n_points: int = 100
) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Compute upper and lower airfoil surface points from 12 CST coefficients.

    Returns (upper_points, lower_points) each as list of (x, y) tuples.
    cst_params[:6] upper surface coefficients, cst_params[6:] lower surface.
    """
    upper_coeffs = cst_params[:6]
    lower_coeffs = cst_params[6:]
    x_coords = _cosine_spacing(n_points)
    upper: list[tuple[float, float]] = []
    lower: list[tuple[float, float]] = []
    for x in x_coords:
        c = _class_function(x)
        yu = c * _shape_function(upper_coeffs, x)
        yl = -c * _shape_function(lower_coeffs, x)
        upper.append((x, yu))
        lower.append((x, yl))
    return upper, lower


# ── 3D wing geometry (T008) ──

def _offset_airfoil_inward(pts: list[tuple[float, float]], dist: float) -> list[tuple[float, float]]:
    """Offset airfoil contour points inward by dist along approximate normals."""
    n = len(pts)
    result = []
    for i in range(n):
        prev = pts[(i - 1) % n]
        curr = pts[i]
        nxt = pts[(i + 1) % n]
        dx = nxt[0] - prev[0]
        dy = nxt[1] - prev[1]
        length = math.sqrt(dx * dx + dy * dy)
        if length < 1e-12:
            result.append(curr)
            continue
        nx = -dy / length
        ny = dx / length
        # Ensure normal points inward (upper y>0 → inward is -y, lower y<0 → inward is +y)
        if curr[1] > 0 and ny > 0:
            nx, ny = -nx, -ny
        elif curr[1] < 0 and ny < 0:
            nx, ny = -nx, -ny
        result.append((curr[0] + dist * nx, curr[1] + dist * ny))
    return result


def _build_skin_from_contours(
    outer_pts: list[tuple[float, float]],
    inner_pts: list[tuple[float, float]],
    span_half: float,
) -> "cq.Workplane":
    import cadquery as cq
    outer_solid = cq.Workplane("XY").polyline(outer_pts).close().extrude(span_half)
    inner_solid = cq.Workplane("XY").polyline(inner_pts).close().extrude(span_half)
    return outer_solid.cut(inner_solid)


def _build_spar(
    inner_pts: list[tuple[float, float]],
    chord_pos: float,
    thickness: float,
    span_half: float,
) -> "cq.Workplane":
    import cadquery as cq
    ys = [p[1] for p in inner_pts]
    y_min = min(ys) + 0.001
    y_max = max(ys) - 0.001
    x = chord_pos
    return (
        cq.Workplane("XY")
        .transformed(offset=(x - thickness / 2, y_min, 0))
        .box(thickness, y_max - y_min, span_half, centered=False)
    )


def _build_rib(
    inner_pts: list[tuple[float, float]],
    chord: float,
    z_pos: float,
    thickness: float,
) -> "cq.Workplane":
    import cadquery as cq
    ys = [p[1] for p in inner_pts]
    y_min = min(ys) + 0.001
    y_max = max(ys) - 0.001
    return (
        cq.Workplane("XY")
        .transformed(offset=(0, y_min, z_pos - thickness / 2))
        .box(chord, y_max - y_min, thickness, centered=False)
    )


def build_wing_3d(
    cst_params: list[float],
    span: float,
    chord: float,
    rear_spar_web_thickness: float,
    rib_thickness: float,
    rib_spacing: float,
) -> "cq.Assembly":
    import cadquery as cq

    span_half = span / 2.0
    skin_t = 0.0015
    front_spar_x = 0.15 * chord
    rear_spar_x = 0.70 * chord
    front_spar_t = rear_spar_web_thickness * 1.5

    upper, lower = cst_to_airfoil_points(cst_params, n_points=100)
    upper_pts: list[tuple[float, float]] = [(p[0], p[1]) for p in upper]
    lower_pts: list[tuple[float, float]] = [(p[0], p[1]) for p in lower]
    # Skip last upper point (TE) to avoid duplicate with first reversed-lower point
    contour = upper_pts[:-1] + list(reversed(lower_pts))

    inner_contour = _offset_airfoil_inward(contour, skin_t)

    skin = _build_skin_from_contours(contour, inner_contour, span_half)
    front_spar = _build_spar(inner_contour, front_spar_x, front_spar_t, span_half)
    rear_spar = _build_spar(inner_contour, rear_spar_x, rear_spar_web_thickness, span_half)

    n_ribs = int(math.ceil(span_half / rib_spacing)) + 1
    ribs: list[cq.Workplane] = []
    for i in range(n_ribs):
        z = i * span_half / max(n_ribs - 1, 1)
        ribs.append(_build_rib(inner_contour, chord, z, rib_thickness))

    assy = cq.Assembly()
    assy.add(skin, name="skin")
    assy.add(front_spar, name="front_spar")
    assy.add(rear_spar, name="rear_spar")
    for i, rib_solid in enumerate(ribs):
        assy.add(rib_solid, name=f"rib_{i}")

    return assy
