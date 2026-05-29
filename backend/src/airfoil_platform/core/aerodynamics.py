"""Core aerodynamics logic: stub predictions."""

import math
import numpy as np
from typing import List

from airfoil_platform.contracts.common import CpPoint
from airfoil_platform.core.geometry import generate_airfoil_2d


def predict_lift_drag_ratio(cst_params: List[float], mach: float, aoa_deg: float) -> float:
    """Stub lift-drag ratio prediction."""
    aoa_rad = math.radians(aoa_deg)
    avg_camber = sum(cst_params[:6]) / 6.0 - sum(cst_params[6:]) / 6.0
    cl = 2.0 * math.pi * (aoa_rad + 0.1 * avg_camber)
    cd = 0.005 + 0.05 * cl * cl
    if cd < 0.001:
        cd = 0.001
    return cl / cd


def predict_cp_distribution(cst_params: List[float]) -> List[CpPoint]:
    """Generate 200 Cp points corresponding to 2D airfoil points."""
    airfoil_points = generate_airfoil_2d(cst_params)
    cp_points = []
    for i, ap in enumerate(airfoil_points):
        # Upper surface (first 100) has lower Cp, lower surface has higher Cp
        if i < 100:
            cp = -0.5 - 0.3 * (1.0 - ap.x)
        else:
            cp = 0.1 + 0.1 * ap.x
        cp_points.append(CpPoint(x=ap.x, y=ap.y, cp=cp))
    return cp_points


def generate_field_data(n_field_points: int = 1000):
    """Generate stub field coordinate, pressure, and velocity arrays."""
    # Cosine-spaced x, clustered near LE and TE
    x = (np.cos(np.linspace(0, 2.0 * math.pi, n_field_points)) + 1.0) / 2.0 * 1.2 - 0.1
    x = np.clip(x, -0.1, 1.1)
    # y follows a decaying pattern away from the airfoil
    y = 0.5 * (np.sin(np.linspace(0, 4.0 * math.pi, n_field_points)) *
               np.exp(-2.0 * np.abs(x - 0.5)))
    coordinates = np.column_stack([x, y]).astype(np.float64)
    pressure = (101325.0 + 500.0 * np.sin(2.0 * math.pi * x) *
                np.exp(-3.0 * np.abs(y))).astype(np.float64)
    velocity = (30.0 + 20.0 * (1.0 - np.abs(x - 0.5)) *
                np.exp(-2.0 * np.abs(y))).astype(np.float64)
    return coordinates, pressure, velocity
