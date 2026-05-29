"""Default values and path configuration."""

import os

# Wing planform defaults
DEFAULT_WING_SPAN = 10.0
DEFAULT_WING_CHORD = 1.0

# Material defaults - skin (aluminum alloy)
DEFAULT_SKIN_ELASTIC_MODULUS_PA = 70_000_000_000
DEFAULT_SKIN_MATERIAL_DENSITY_KG_M3 = 2700

# Material defaults - internal structure (structural steel)
DEFAULT_INTERNAL_STRUCTURE_ELASTIC_MODULUS_PA = 200_000_000_000
DEFAULT_INTERNAL_STRUCTURE_MATERIAL_DENSITY_KG_M3 = 7850

# Gravity
G = 9.80665

# Artifact root (relative to backend/)
ARTIFACT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..", "runtime_artifacts")

# Stub mode
STUB_MODE = True
STUB_MODEL_VERSION = "stub-v0"

# Fixed structural assumptions
SKIN_THICKNESS = 0.0015
FRONT_SPAR_CHORD_FRACTION = 0.15
REAR_SPAR_CHORD_FRACTION = 0.70
FRONT_SPAR_WEB_THICKNESS_RATIO = 1.5

# Wing planform validation ranges
SPAN_MIN = 0.0  # exclusive
SPAN_MAX = 100.0
CHORD_MIN = 0.0  # exclusive
CHORD_MAX = 20.0

# Structure design validation ranges
REAR_SPAR_WEB_THICKNESS_MIN = 0.002
REAR_SPAR_WEB_THICKNESS_MAX = 0.020
RIB_THICKNESS_MIN = 0.002
RIB_THICKNESS_MAX = 0.005
RIB_SPACING_MIN = 0.300
RIB_SPACING_MAX = 1.000
