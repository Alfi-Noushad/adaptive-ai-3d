from pathlib import Path

from fastapi import APIRouter

from mesh.api.routes_analysis import MeshPathRequest
from mesh.optimizer.mesh_optimizer import optimize_mesh
from mesh.utils.response import success_response
from mesh.utils.storage import STORAGE_ROOT, resolve_mesh_path

router = APIRouter()


class OptimizeRequest(MeshPathRequest):
    target_faces: int | None = None
    smooth: bool = False


@router.post("/optimize")
def optimize(req: OptimizeRequest):
    path = Path(resolve_mesh_path(req.mesh_path))
    out = path.with_name(f"{path.stem}_optimized.ply")

    result = optimize_mesh(str(path), str(out), req.target_faces, req.smooth)
    result["optimized_mesh_path"] = out.relative_to(STORAGE_ROOT).as_posix()
    return success_response(result, "Mesh optimized")