import pytest
from pydantic import ValidationError

from airfoil_platform.contracts import (
    validate_cst_12,
    validate_ratio,
    WingPlanform,
    StructureDesign,
)
from airfoil_platform.config.settings import (
    DEFAULT_WING_SPAN,
    DEFAULT_WING_CHORD,
    SPAN_MAX,
    CHORD_MAX,
    REAR_SPAR_WEB_THICKNESS_MIN,
    REAR_SPAR_WEB_THICKNESS_MAX,
    RIB_THICKNESS_MIN,
    RIB_THICKNESS_MAX,
    RIB_SPACING_MIN,
    RIB_SPACING_MAX,
)


# --- CST params ---


def test_cst_12_valid():
    assert validate_cst_12([0.1] * 12) == [0.1] * 12


def test_cst_11_rejected():
    with pytest.raises(ValueError, match="exactly 12"):
        validate_cst_12([0.1] * 11)


def test_cst_13_rejected():
    with pytest.raises(ValueError, match="exactly 12"):
        validate_cst_12([0.1] * 13)


def test_cst_empty_rejected():
    with pytest.raises(ValueError, match="exactly 12"):
        validate_cst_12([])


# --- Ratio ---


def test_ratio_valid():
    assert validate_ratio(0.5) == 0.5
    assert validate_ratio(1.0) == 1.0
    assert validate_ratio(0.01) == 0.01


def test_ratio_zero_rejected():
    with pytest.raises(ValueError, match="0 < ratio <= 1"):
        validate_ratio(0.0)


def test_ratio_negative_rejected():
    with pytest.raises(ValueError, match="0 < ratio <= 1"):
        validate_ratio(-0.1)


def test_ratio_greater_than_one_rejected():
    with pytest.raises(ValueError, match="0 < ratio <= 1"):
        validate_ratio(1.1)


# --- WingPlanform ---


def test_wing_planform_defaults():
    wp = WingPlanform()
    assert wp.span == DEFAULT_WING_SPAN
    assert wp.chord == DEFAULT_WING_CHORD


def test_wing_planform_custom():
    wp = WingPlanform(span=20.0, chord=5.0)
    assert wp.span == 20.0
    assert wp.chord == 5.0


def test_wing_planform_partial_override():
    wp = WingPlanform(chord=3.0)
    assert wp.span == DEFAULT_WING_SPAN
    assert wp.chord == 3.0


@pytest.mark.parametrize("invalid_span", [0.0, -1.0, 100.1, 200.0])
def test_span_out_of_range_rejected(invalid_span):
    with pytest.raises(ValidationError):
        WingPlanform(span=invalid_span)


def test_span_at_boundaries():
    WingPlanform(span=0.001)
    WingPlanform(span=SPAN_MAX)


@pytest.mark.parametrize("invalid_chord", [0.0, -1.0, 20.1, 50.0])
def test_chord_out_of_range_rejected(invalid_chord):
    with pytest.raises(ValidationError):
        WingPlanform(chord=invalid_chord)


def test_chord_at_boundaries():
    WingPlanform(chord=0.001)
    WingPlanform(chord=CHORD_MAX)


# --- StructureDesign ---


def test_structure_design_valid():
    sd = StructureDesign(
        rear_spar_web_thickness=0.005,
        rib_thickness=0.003,
        rib_spacing=0.500,
    )
    assert sd.rear_spar_web_thickness == 0.005
    assert sd.rib_thickness == 0.003
    assert sd.rib_spacing == 0.500


def test_structure_design_missing_fields():
    with pytest.raises(ValidationError):
        StructureDesign(rear_spar_web_thickness=0.005)
    with pytest.raises(ValidationError):
        StructureDesign(rib_thickness=0.003)
    with pytest.raises(ValidationError):
        StructureDesign(rib_spacing=0.500)


def test_structure_design_at_boundaries():
    StructureDesign(
        rear_spar_web_thickness=REAR_SPAR_WEB_THICKNESS_MIN,
        rib_thickness=RIB_THICKNESS_MIN,
        rib_spacing=RIB_SPACING_MIN,
    )
    StructureDesign(
        rear_spar_web_thickness=REAR_SPAR_WEB_THICKNESS_MAX,
        rib_thickness=RIB_THICKNESS_MAX,
        rib_spacing=RIB_SPACING_MAX,
    )


@pytest.mark.parametrize("bad_thickness", [0.001, 0.021])
def test_rear_spar_web_thickness_out_of_range(bad_thickness):
    with pytest.raises(ValidationError):
        StructureDesign(
            rear_spar_web_thickness=bad_thickness,
            rib_thickness=0.003,
            rib_spacing=0.500,
        )


@pytest.mark.parametrize("bad_thickness", [0.001, 0.006])
def test_rib_thickness_out_of_range(bad_thickness):
    with pytest.raises(ValidationError):
        StructureDesign(
            rear_spar_web_thickness=0.005,
            rib_thickness=bad_thickness,
            rib_spacing=0.500,
        )


@pytest.mark.parametrize("bad_spacing", [0.200, 1.100])
def test_rib_spacing_out_of_range(bad_spacing):
    with pytest.raises(ValidationError):
        StructureDesign(
            rear_spar_web_thickness=0.005,
            rib_thickness=0.003,
            rib_spacing=bad_spacing,
        )
