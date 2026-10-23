from fastapi import APIRouter
from pydantic import BaseModel

from mesh.analysis.failure_detection import detect_failures
from mesh.analysis.mesh_analysis import analyze_mesh
from mesh.analysis.mesh_quality import evaluate_mesh_quality
from mesh.utils.response import success_response
from mesh.utils.storage import resolve_mesh_path

router = APIRouter()


class MeshReportRequest(BaseModel):
    mesh_path: str


@router.post("/report")
def report(req: MeshReportRequest):
    path = resolve_mesh_path(req.mesh_path)
    return success_response(
        {
            "analysis": analyze_mesh(path),
            "quality": evaluate_mesh_quality(path),
            "failures": detect_failures(path),
        },
        "Mesh report generated",
    )
