from fastapi import APIRouter
from pydantic import BaseModel

from mesh.analysis.mesh_analysis import analyze_mesh
from mesh.analysis.mesh_quality import evaluate_mesh_quality
from mesh.utils.response import success_response
from mesh.utils.storage import resolve_mesh_path
from mesh.analysis.failure_detection import detect_failures


router = APIRouter()


class MeshPathRequest(BaseModel):
    mesh_path: str


@router.post("/analyze")
def analyze(req: MeshPathRequest):
    path = resolve_mesh_path(req.mesh_path)
    return success_response(analyze_mesh(path), "Mesh analysis complete")


@router.post("/evaluate")
def evaluate(req: MeshPathRequest):
    path = resolve_mesh_path(req.mesh_path)
    return success_response(evaluate_mesh_quality(path), "Mesh quality evaluation complete")


@router.post("/evaluate")
def evaluate(req: MeshPathRequest):
    path = resolve_mesh_path(req.mesh_path)
    result = evaluate_mesh_quality(path)
    result["defect_report"] = detect_failures(path)
    return success_response(result, "Mesh quality evaluation complete")