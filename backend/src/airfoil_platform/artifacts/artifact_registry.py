from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Optional


@dataclass
class ArtifactMetadata:
    artifact_id: str
    format: str
    role: str
    path: str
    status: str = "ready"
    datasets: Optional[list[str]] = None
    components: Optional[list[str]] = None


class ArtifactRegistry:

    def __init__(self, artifact_root: str):
        self._artifact_root = Path(artifact_root)
        self._cache: dict[str, ArtifactMetadata] = {}

    def register(self, metadata: ArtifactMetadata) -> None:
        self._cache[metadata.artifact_id] = metadata

    def get(self, artifact_id: str) -> Optional[ArtifactMetadata]:
        if artifact_id in self._cache:
            return self._cache[artifact_id]
        return self._read_sidecar(artifact_id)

    def _read_sidecar(self, artifact_id: str) -> Optional[ArtifactMetadata]:
        for role_dir in ["aerodynamic", "geometry"]:
            sidecar_path = self._artifact_root / role_dir / f"{artifact_id}.json"
            if sidecar_path.exists():
                data = json.loads(sidecar_path.read_text())
                meta = ArtifactMetadata(**data)
                self._cache[artifact_id] = meta
                return meta
        return None
