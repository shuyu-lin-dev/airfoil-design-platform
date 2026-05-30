from __future__ import annotations

import math


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
