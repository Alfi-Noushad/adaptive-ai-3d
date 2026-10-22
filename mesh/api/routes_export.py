from pathlib import Path

from fastapi import APIRouter, HTTPException

from mesh.api.routes_analysis import MeshPathRequest
from mesh.exports.exporter import SUPPORTED_FORMATS, export_mesh
from mesh.utils.response import success_response
from mesh.utils.storage import STORAGE_ROOT, resolve_mesh_path

router = APIRouter()


class ExportRequest(MeshPathRequest):
    format: str = "glb"


@router.post("/export")
def export(req: ExportRequest):
    fmt = req.format.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{fmt}'. Supported: {sorted(SUPPORTED_FORMATS)}",
        )

    path = Path(resolve_mesh_path(req.mesh_path))
    out = path.with_suffix(f".{fmt}")

    result = export_mesh(str(path), str(out), fmt)
    result["export_path"] = out.relative_to(STORAGE_ROOT).as_posix()
    return success_response(result, f"Mesh exported as {fmt.upper()}")