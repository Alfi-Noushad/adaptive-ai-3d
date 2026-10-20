from pathlib import Path

from fastapi import APIRouter

from mesh.api.routes_analysis import MeshPathRequest
from mesh.repair.self_healing import repair_mesh
from mesh.utils.response import success_response
from mesh.utils.storage import STORAGE_ROOT, resolve_mesh_path

router = APIRouter()


@router.post("/repair")
def repair(req: MeshPathRequest):
    path = Path(resolve_mesh_path(req.mesh_path))
    out = path.with_name(f"{path.stem}_repaired.ply")

    result = repair_mesh(str(path), str(out))
    result["repaired_mesh_path"] = out.relative_to(STORAGE_ROOT).as_posix()

    msg = "Mesh repaired" if not result["unresolved"] else "Mesh repaired with unresolved defects"
    return success_response(result, msg)