"""Tests for CST param and ratio validation."""

import pytest

from airfoil_platform.contracts.common import (
    StubMeta,
    validate_cst_params,
    validate_ratio,
    CST_PARAMS_COUNT,
)


# ---- CST params ----

def test_cst_params_exactly_12():
    valid = [0.1] * 12
    assert validate_cst_params(valid) == valid


def test_cst_params_too_few():
    with pytest.raises(ValueError, match="exactly 12"):
        validate_cst_params([0.1] * 11)


def test_cst_params_too_many():
    with pytest.raises(ValueError, match="exactly 12"):
        validate_cst_params([0.1] * 13)


# ---- Ratio ----

def test_ratio_valid():
    assert validate_ratio(0.1) == 0.1
    assert validate_ratio(1.0) == 1.0
    assert validate_ratio(0.001) == 0.001


def test_ratio_zero():
    with pytest.raises(ValueError, match="ratio must be in"):
        validate_ratio(0.0)


def test_ratio_negative():
    with pytest.raises(ValueError, match="ratio must be in"):
        validate_ratio(-0.1)


def test_ratio_above_one():
    with pytest.raises(ValueError, match="ratio must be in"):
        validate_ratio(1.5)


# ---- StubMeta ----

def test_stub_meta_defaults():
    meta = StubMeta()
    assert meta.is_stub is True
    assert meta.model_version == "stub-v0"
