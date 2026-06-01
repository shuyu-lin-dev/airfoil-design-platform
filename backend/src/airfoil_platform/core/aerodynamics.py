from __future__ import annotations

import math

import numpy as np

from airfoil_platform.contracts.geometry import AirfoilPoint


def compute_lift_drag_ratio(
    cst_params: list[float], mach: float, angle_of_attack_deg: float
) -> float:
    aoa_rad = math.radians(angle_of_attack_deg)
    upper_mean = sum(cst_params[:6]) / 6.0
    lower_mean = sum(cst_params[6:]) / 6.0
    camber_effect = (upper_mean - lower_mean) * 10.0
    cl = 0.5 + 2.0 * math.pi * aoa_rad + camber_effect
    cd = 0.01 + 0.01 * cl ** 2
    return cl / cd


def compute_cp_distribution(
    points: list[AirfoilPoint], mach: float, angle_of_attack_deg: float
) -> list[dict]:
    aoa_rad = math.radians(angle_of_attack_deg)
    result = []
    for pt in points:
        cp = 1.0 - pt.x ** 2 - 0.2 * math.sin(aoa_rad) * (pt.y / 0.1) if abs(pt.y) > 1e-12 else 1.0 - pt.x ** 2
        result.append({"x": pt.x, "cp": round(cp, 6)})
    return result


def _nearest_airfoil_distance(x: float, y: float, pts: list[AirfoilPoint]) -> float:
    min_d2 = float("inf")
    for p in pts:
        d2 = (x - p.x) ** 2 + (y - p.y) ** 2
        if d2 < min_d2:
            min_d2 = d2
    return math.sqrt(min_d2)


def generate_field_data(
    airfoil_points: list[AirfoilPoint], mach: float, angle_of_attack_deg: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_range = np.linspace(-0.2, 1.2, 40)
    y_range = np.linspace(-0.6, 0.6, 25)
    xx, yy = np.meshgrid(x_range, y_range)
    coords = np.column_stack([xx.ravel(), yy.ravel()])  # (1000, 2)

    pressure = np.zeros(1000, dtype=np.float64)
    velocity = np.zeros(1000, dtype=np.float64)
    aoa_rad = math.radians(angle_of_attack_deg)

    for i in range(1000):
        d = _nearest_airfoil_distance(coords[i, 0], coords[i, 1], airfoil_points)
        d = max(d, 0.001)  # avoid division by zero on the surface
        pressure[i] = 101325.0 * (1.0 - 0.3 * mach ** 2 / (d + 0.01))
        velocity[i] = 50.0 * mach * math.cos(aoa_rad) / (d + 0.01)

    return coords, pressure, velocity
