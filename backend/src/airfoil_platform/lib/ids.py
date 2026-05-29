"""Artifact ID generation from normalized input parameters."""

import hashlib
import json


def generate_artifact_id(inputs: dict) -> str:
    """
    Generate artifact_id by normalizing input dict (sorted keys),
    serializing to JSON with sorted keys, then SHA-256, taking first 12 hex chars.
    """
    normalized = json.dumps(inputs, sort_keys=True, allow_nan=False)
    sha = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return sha[:12]
