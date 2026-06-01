from __future__ import annotations

import math


def _cosine_spacing(n: int) -> list[float]:
    return [(1.0 - math.cos(i * math.pi / (n - 1))) / 2.0 for i in range(n)]


def generate_airfoil_from_control_points(
    camber_cp: list[dict], thickness_cp: list[dict], n_points: int = 100
) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Stub: linear camber line + parabolic thickness distribution."""
    x_coords = _cosine_spacing(n_points)

    # Linear camber line through two control points
    (x0, y0), (x1, y1) = (camber_cp[0]["x"], camber_cp[0]["y"]), (camber_cp[1]["x"], camber_cp[1]["y"])
    slope = (y1 - y0) / max(x1 - x0, 1e-12)

    def camber(x):
        return y0 + slope * (x - x0)

    # Thickness: parabolic through two control points, zero at LE and TE
    (tx0, ty0), (tx1, ty1) = (thickness_cp[0]["x"], thickness_cp[0]["y"]), (thickness_cp[1]["x"], thickness_cp[1]["y"])
    t_slope = (ty1 - ty0) / max(tx1 - tx0, 1e-12)

    def half_thickness(x):
        base = ty0 + t_slope * (x - tx0)
        return base * 4.0 * x * (1.0 - x)

    upper = []
    lower = []
    for x in x_coords:
        c = camber(x)
        t = half_thickness(x)
        upper.append((x, c + t))
        lower.append((x, c - t))

    return upper, lower


def approximate_cst_from_points(points: list[dict]) -> list[float]:
    """Stub: extract 12 CST params by sampling y at 6 x positions for upper/lower."""
    n = len(points)
    half = n // 2
    upper = points[:half]
    lower = points[half:]

    # Sample 6 evenly spaced x positions
    sample_indices = [int(i * (half - 1) / 5.0) for i in range(6)]

    upper_cst = []
    lower_cst = []
    for idx in sample_indices:
        idx = min(idx, half - 1)
        x = upper[idx]["x"]
        y = upper[idx]["y"]
        # Rough inverse: at x, class_function * shape ≈ y, shape ≈ y / class_fn
        cf = (x ** 0.5) * ((1.0 - x) ** 1.0)
        upper_cst.append(round(y / max(cf, 1e-12), 6))

    for idx in sample_indices:
        idx = min(idx, half - 1)
        x = lower[idx]["x"]
        y = lower[idx]["y"]
        cf = (x ** 0.5) * ((1.0 - x) ** 1.0)
        lower_cst.append(round(abs(y) / max(cf, 1e-12), 6))

    return upper_cst + lower_cst
