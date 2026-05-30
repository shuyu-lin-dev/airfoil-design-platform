import pytest
from pydantic import ValidationError

from airfoil_platform.contracts import (
    MaterialGroup,
    MaterialProperties,
    ConditionParams,
    ResultMeta,
)
from airfoil_platform.config.settings import STUB_MODEL_VERSION


# --- MaterialGroup ---


def test_material_group_valid():
    mg = MaterialGroup(elastic_modulus=70e9, material_density=2700)
    assert mg.elastic_modulus == 70e9
    assert mg.material_density == 2700


def test_material_group_missing_fields():
    with pytest.raises(ValidationError):
        MaterialGroup(elastic_modulus=70e9)
    with pytest.raises(ValidationError):
        MaterialGroup(material_density=2700)


def test_material_group_zero_or_negative_rejected():
    with pytest.raises(ValidationError):
        MaterialGroup(elastic_modulus=0, material_density=2700)
    with pytest.raises(ValidationError):
        MaterialGroup(elastic_modulus=70e9, material_density=-1)


# --- MaterialProperties ---


def test_material_properties_full():
    mp = MaterialProperties(
        skin=MaterialGroup(elastic_modulus=70e9, material_density=2700),
        internal_structure=MaterialGroup(elastic_modulus=200e9, material_density=7850),
    )
    assert mp.skin.elastic_modulus == 70e9
    assert mp.internal_structure.material_density == 7850


def test_material_properties_fully_optional():
    mp = MaterialProperties()
    assert mp.skin is None
    assert mp.internal_structure is None


def test_material_properties_partial_skin_only():
    mp = MaterialProperties(skin=MaterialGroup(elastic_modulus=70e9, material_density=2700))
    assert mp.skin is not None
    assert mp.internal_structure is None


# --- ConditionParams ---


def test_condition_params():
    cp = ConditionParams(mach=0.5, angle_of_attack=3.0)
    assert cp.mach == 0.5
    assert cp.angle_of_attack == 3.0


def test_condition_params_missing():
    with pytest.raises(ValidationError):
        ConditionParams(mach=0.5)
    with pytest.raises(ValidationError):
        ConditionParams(angle_of_attack=3.0)


# --- ResultMeta ---


def test_result_meta_defaults():
    meta = ResultMeta()
    assert meta.is_stub is True
    assert meta.model_version == STUB_MODEL_VERSION


def test_result_meta_custom():
    meta = ResultMeta(is_stub=False, model_version="v1.0")
    assert meta.is_stub is False
    assert meta.model_version == "v1.0"
