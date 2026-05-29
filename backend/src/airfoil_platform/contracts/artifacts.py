"""Contracts for artifact query/download endpoints."""

from typing import Optional, List, Dict
from pydantic import BaseModel


class ArtifactMetaResponse(BaseModel):
    artifact_id: str
    status: str
    format: str
    role: str
    path: str
    datasets: Optional[Dict[str, str]] = None
    components: Optional[List[str]] = None
