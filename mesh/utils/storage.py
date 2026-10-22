import os
from pathlib import Path

from fastapi import HTTPException

STORAGE_ROOT = Path(os.getenv("MESH_STORAGE_ROOT", "storage")).resolve()


def resolve_mesh_path(mesh_path: str) -> str:
    """Resolve a Backend-supplied path inside STORAGE_ROOT, or raise."""
    candidate = (STORAGE_ROOT / mesh_path).resolve()

    if not candidate.is_relative_to(STORAGE_ROOT):
        raise HTTPException(status_code=400, detail="mesh_path is outside storage root")
    if not candidate.is_file():
        raise HTTPException(status_code=404, detail=f"Mesh file not found: {mesh_path}")

    return str(candidate)