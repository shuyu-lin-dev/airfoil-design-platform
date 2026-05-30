"""Core geometry logic: 2D CST airfoil parameterization."""

import math
from typing import List

from airfoil_platform.contracts.common import Point2D


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
