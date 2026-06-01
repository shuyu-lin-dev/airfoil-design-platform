from __future__ import annotations

import math

from airfoil_platform.config.settings import (
    DEFAULT_INTERNAL_ELASTIC_MODULUS,
    DEFAULT_INTERNAL_MATERIAL_DENSITY,
    DEFAULT_SKIN_ELASTIC_MODULUS,
    DEFAULT_SKIN_MATERIAL_DENSITY,
    GRAVITY_ACCELERATION,
    SKIN_THICKNESS,
)


def compute_weight(
    cst_params: list[float],
    span: float,
    chord: float,
    rear_spar_web_thickness: float,
    rib_thickness: float,
    rib_spacing: float,
    skin_density: float = DEFAULT_SKIN_MATERIAL_DENSITY,
    internal_density: float = DEFAULT_INTERNAL_MATERIAL_DENSITY,
) -> float:
    span_half = span / 2.0
    front_spar_t = rear_spar_web_thickness * 1.5
    n_ribs = int(math.ceil(span_half / rib_spacing)) + 1

    # Approximate airfoil perimeter and area from CST params
    upper_mean = sum(abs(v) for v in cst_params[:6]) / 6.0
    lower_mean = sum(abs(v) for v in cst_params[6:]) / 6.0
    camber = (upper_mean + lower_mean) / 2.0
    perimeter = 2.0 * chord + 0.5 * chord * camber
    area = 0.08 * chord * chord + 0.05 * chord * chord * camber

    y_range = 0.1 * chord * (1.0 + camber * 5.0)

    skin_vol = perimeter * span_half * SKIN_THICKNESS
    fs_vol = y_range * span_half * front_spar_t
    rs_vol = y_range * span_half * rear_spar_web_thickness
    rib_vol = area * rib_thickness * n_ribs

    total_mass = skin_vol * skin_density + (fs_vol + rs_vol + rib_vol) * internal_density
    return round(total_mass * GRAVITY_ACCELERATION, 2)


def compute_max_stress(
    cst_params: list[float],
    span: float,
    chord: float,
    mach: float,
    angle_of_attack_deg: float,
    rear_spar_web_thickness: float,
    rib_thickness: float,
    skin_elastic_modulus: float = DEFAULT_SKIN_ELASTIC_MODULUS,
    internal_elastic_modulus: float = DEFAULT_INTERNAL_ELASTIC_MODULUS,
) -> float:
    span_half = span / 2.0
    front_spar_t = rear_spar_web_thickness * 1.5

    upper_mean = sum(abs(v) for v in cst_params[:6]) / 6.0
    lower_mean = sum(abs(v) for v in cst_params[6:]) / 6.0
    camber = (upper_mean + lower_mean) / 2.0
    y_range = 0.1 * chord * (1.0 + camber * 5.0)

    # Approximate lift as distributed load
    aoa_rad = math.radians(angle_of_attack_deg)
    cl = 0.5 + 2.0 * math.pi * aoa_rad
    dynamic_pressure = 0.5 * 1.225 * (mach * 340.0) ** 2
    lift_per_span = cl * dynamic_pressure * chord
    moment = lift_per_span * span_half ** 2 / 2.0

    # Simplified second moment of area
    i_xx = (y_range ** 3 / 12.0) * (SKIN_THICKNESS * 2.0 + front_spar_t + rear_spar_web_thickness)
    stress = moment * (y_range / 2.0) / max(i_xx, 1e-12)
    return round(stress, 2)
