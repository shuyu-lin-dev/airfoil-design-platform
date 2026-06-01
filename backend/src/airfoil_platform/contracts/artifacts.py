from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ArtifactMetadataResponse(BaseModel):
    artifact_id: str
    format: str
    role: str
    path: str
    status: str
    datasets: Optional[list[str]] = None
    components: Optional[list[str]] = None
