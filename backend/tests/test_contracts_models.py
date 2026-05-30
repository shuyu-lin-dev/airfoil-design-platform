"""Tests for Pydantic contract models."""

import pytest
from pydantic import ValidationError

from airfoil_platform.contracts.common import (
    Condition,
    WingPlanform,
    StructureDesign,
    MaterialGroup,
    MaterialProperties,
    TeachingControlPoint,
)
from airfoil_platform.config import settings


# ---- Condition ----

def test_condition_valid():
    c = Condition(mach=0.3, angle_of_attack=2.0)
    assert c.mach == 0.3
    assert c.angle_of_attack == 2.0


# ---- WingPlanform ----

def test_wing_planform_defaults():
    wp = WingPlanform()
    assert wp.span == settings.DEFAULT_WING_SPAN
    assert wp.chord == settings.DEFAULT_WING_CHORD


def test_wing_planform_null_uses_defaults():
    wp = WingPlanform(span=None, chord=None)
    assert wp.span == settings.DEFAULT_WING_SPAN
    assert wp.chord == settings.DEFAULT_WING_CHORD


def test_wing_planform_custom_values():
    wp = WingPlanform(span=20.0, chord=5.0)
    assert wp.span == 20.0
    assert wp.chord == 5.0


def test_wing_planform_span_zero_rejected():
    with pytest.raises(ValidationError):
        WingPlanform(span=0.0)


def test_wing_planform_span_negative_rejected():
    with pytest.raises(ValidationError):
        WingPlanform(span=-1.0)


def test_wing_planform_span_exceeds_max():
    with pytest.raises(ValidationError):
        WingPlanform(span=101.0)


def test_wing_planform_chord_zero_rejected():
    with pytest.raises(ValidationError):
        WingPlanform(chord=0.0)


def test_wing_planform_chord_exceeds_max():
    with pytest.raises(ValidationError):
        WingPlanform(chord=21.0)


# ---- StructureDesign ----

def test_structure_design_valid():
    sd = StructureDesign(rear_spar_web_thickness=0.005, rib_thickness=0.003, rib_spacing=0.5)
    assert sd.rear_spar_web_thickness == 0.005
    assert sd.rib_thickness == 0.003
    assert sd.rib_spacing == 0.5


def test_structure_design_all_fields_required():
    with pytest.raises(ValidationError):
        StructureDesign(rear_spar_web_thickness=0.005, rib_thickness=0.003)


@pytest.mark.parametrize("field,value", [
    ("rear_spar_web_thickness", 0.001),
    ("rear_spar_web_thickness", 0.021),
    ("rib_thickness", 0.001),
    ("rib_thickness", 0.006),
    ("rib_spacing", 0.200),
    ("rib_spacing", 1.100),
])
def test_structure_design_range_validation(field, value):
    kwargs = {"rear_spar_web_thickness": 0.005, "rib_thickness": 0.003, "rib_spacing": 0.5}
    kwargs[field] = value
    with pytest.raises(ValidationError):
        StructureDesign(**kwargs)


# ---- MaterialGroup ----

def test_material_group_valid():
    mg = MaterialGroup(elastic_modulus=70e9, material_density=2700)
    assert mg.elastic_modulus == 70e9
    assert mg.material_density == 2700


def test_material_group_requires_both_fields():
    with pytest.raises(ValidationError):
        MaterialGroup(elastic_modulus=70e9)


def test_material_group_positive_values():
    with pytest.raises(ValidationError):
        MaterialGroup(elastic_modulus=0, material_density=2700)
    with pytest.raises(ValidationError):
        MaterialGroup(elastic_modulus=70e9, material_density=-1)


# ---- MaterialProperties ----

def test_material_properties_defaults():
    mp = MaterialProperties()
    skin = mp.get_skin()
    internal = mp.get_internal_structure()
    assert skin.elastic_modulus == settings.DEFAULT_SKIN_ELASTIC_MODULUS_PA
    assert skin.material_density == settings.DEFAULT_SKIN_MATERIAL_DENSITY_KG_M3
    assert internal.elastic_modulus == settings.DEFAULT_INTERNAL_STRUCTURE_ELASTIC_MODULUS_PA
    assert internal.material_density == settings.DEFAULT_INTERNAL_STRUCTURE_MATERIAL_DENSITY_KG_M3


def test_material_properties_full_override():
    mp = MaterialProperties(
        skin=MaterialGroup(elastic_modulus=1e9, material_density=1000),
        internal_structure=MaterialGroup(elastic_modulus=2e9, material_density=2000),
    )
    assert mp.get_skin().elastic_modulus == 1e9
    assert mp.get_internal_structure().elastic_modulus == 2e9


def test_material_properties_partial_override():
    mp = MaterialProperties(
        skin=MaterialGroup(elastic_modulus=1e9, material_density=1000),
    )
    skin = mp.get_skin()
    internal = mp.get_internal_structure()
    assert skin.elastic_modulus == 1e9
    assert internal.elastic_modulus == settings.DEFAULT_INTERNAL_STRUCTURE_ELASTIC_MODULUS_PA


def test_material_properties_omitted():
    mp = MaterialProperties()
    assert mp.skin is None
    assert mp.internal_structure is None
    assert mp.get_skin().elastic_modulus == settings.DEFAULT_SKIN_ELASTIC_MODULUS_PA


# ---- TeachingControlPoint ----

def test_teaching_control_point_valid():
    cp = TeachingControlPoint(x=0.5, y=0.02)
    assert cp.x == 0.5
    assert cp.y == 0.02


def test_teaching_control_point_x_range():
    with pytest.raises(ValidationError):
        TeachingControlPoint(x=-0.1, y=0.0)
    with pytest.raises(ValidationError):
        TeachingControlPoint(x=1.1, y=0.0)
