import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from urllib.parse import quote

from app.services.mesh_client import mesh_client, MeshServiceError

from app.database.session import get_db
from app.models.entities import (
    Project, Image, GeneratedMesh, AIEvaluationReport,
    MeshQualityReport, Recommendation, Feedback, PromptEdit, ExportJob
)
from app.core.response import api_response

router = APIRouter(tags=["Projects & Pipeline Contract"])

class PromptEditRequest(BaseModel):
    project_id: int
    prompt: str

class FeedbackRequest(BaseModel):
    project_id: int
    rating: int
    comment: Optional[str] = None
    user_id: Optional[int] = None

@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    results = [
        {
            "id": p.id,
            "title": p.title,
            "status": p.status,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in projects
    ]
    return api_response(
        status="success",
        message="Projects retrieved successfully",
        data=results
    )

@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return api_response(
        status="success",
        message="Project details retrieved",
        data={
            "id": project.id,
            "title": project.title,
            "status": project.status,
            "user_id": project.user_id,
            "created_at": project.created_at.isoformat() if project.created_at else None
        }
    )

@router.get("/projects/{project_id}/report")
def get_merged_project_report(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ai_report = db.query(AIEvaluationReport).filter(AIEvaluationReport.project_id == project_id).first()
    mesh_report = db.query(MeshQualityReport).filter(MeshQualityReport.project_id == project_id).first()
    mesh_versions = db.query(GeneratedMesh).filter(
        GeneratedMesh.project_id == project_id
    ).order_by(GeneratedMesh.version.asc()).all()
    preview_mesh = next(
        (item for item in reversed(mesh_versions) if item.mesh_type == "optimized"),
        mesh_versions[-1] if mesh_versions else None,
    )
    preview_path = (
        f"/mesh-assets/{quote(preview_mesh.storage_path.rsplit('.', 1)[0] + '.glb', safe='/')}"
        if preview_mesh else None
    )
    if preview_mesh:
        storage_root = Path(os.getenv(
            "MESH_STORAGE_ROOT", str(Path(__file__).resolve().parents[3] / "storage")
        )).resolve()
        glb_path = (storage_root / (preview_mesh.storage_path.rsplit('.', 1)[0] + ".glb")).resolve()
        if not glb_path.is_relative_to(storage_root) or not glb_path.is_file():
            preview_path = None

    merged_report = {
        "project_id": project_id,
        "optimized_mesh_url": preview_path,
        "ai_evaluation_report": {
            "classification": ai_report.classification if ai_report else None,
            "quality_score": ai_report.quality_score if ai_report else None,
            "selected_model": ai_report.selected_model if ai_report else None,
            "reasoning_xai": ai_report.reasoning_xai if ai_report else None,
            "confidence_scores": ai_report.confidence_scores if ai_report else None
        },
        "mesh_quality_report": ({
            "topology_grade": mesh_report.topology_grade,
            "defect_list": mesh_report.defect_list,
            "repair_actions_taken": mesh_report.repair_actions_taken,
            "optimization_stats": mesh_report.optimization_stats
        } if mesh_report else None),
        "generated_meshes": [
            {
                "mesh_type": item.mesh_type,
                "version": item.version,
                "storage_path": item.storage_path,
                "vertex_count": item.vertex_count,
                "face_count": item.face_count,
            }
            for item in mesh_versions
        ],
    }

    return api_response(
        status="success",
        message="Merged AI and Mesh evaluation reports retrieved",
        data=merged_report
    )

@router.get("/history")
def get_project_history(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    history = [
        {
            "project_id": p.id,
            "title": p.title,
            "status": p.status,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in projects
    ]
    return api_response(
        status="success",
        message="History log retrieved",
        data=history
    )

@router.post("/prompt-edit")
def submit_prompt_edit(edit: PromptEditRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == edit.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    prompt_record = PromptEdit(
        project_id=edit.project_id,
        prompt_text=edit.prompt,
        edit_status="queued"
    )
    db.add(prompt_record)
    db.commit()
    db.refresh(prompt_record)

    return api_response(
        status="success",
        message="Prompt edit queued for Mesh layer processing",
        data={"edit_id": prompt_record.id, "project_id": edit.project_id, "prompt": edit.prompt, "status": "queued"}
    )

@router.post("/feedback")
def submit_feedback(fb: FeedbackRequest, db: Session = Depends(get_db)):
    feedback_record = Feedback(
        project_id=fb.project_id,
        user_id=fb.user_id,
        rating=fb.rating,
        comment=fb.comment
    )
    db.add(feedback_record)
    db.commit()
    db.refresh(feedback_record)

    return api_response(
        status="success",
        message="Feedback logged successfully",
        data={"feedback_id": feedback_record.id, "rating": feedback_record.rating}
    )

@router.get("/recommendations/{project_id}")
def get_recommendations(project_id: int, db: Session = Depends(get_db)):
    recs = db.query(Recommendation).filter(Recommendation.project_id == project_id).all()
    data = [
        {"id": r.id, "category": r.category, "suggestion": r.suggestion_text}
        for r in recs
    ] if recs else [
        {"category": "material", "suggestion": "Apply PBR metallic roughness texture map for realistic rendering."},
        {"category": "topology", "suggestion": "Quad-dominant remeshing recommended for rigging."}
    ]

    return api_response(
        status="success",
        message="Recommendations retrieved",
        data=data
    )

@router.post("/export/{format}")
async def request_mesh_export(format: str, project_id: int, db: Session = Depends(get_db)):
    valid_formats = {"glb"}
    if format.lower() not in valid_formats:
        raise HTTPException(status_code=400, detail=f"Unsupported format '{format}'. Mesh export currently supports GLB.")

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    mesh = db.query(GeneratedMesh).filter(
        GeneratedMesh.project_id == project_id
    ).order_by(GeneratedMesh.version.desc()).first()
    if not mesh:
        raise HTTPException(status_code=409, detail="This project does not have a generated mesh to export yet.")

    export_record = ExportJob(
        project_id=project_id,
        export_format=format.upper(),
        status="running"
    )
    db.add(export_record)
    db.commit()
    db.refresh(export_record)

    try:
        result = await mesh_client.export_mesh(mesh.storage_path, format.lower())
    except MeshServiceError as exc:
        export_record.status = "failed"
        db.commit()
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    export_path = result.get("export_path")
    if not isinstance(export_path, str) or not export_path:
        export_record.status = "failed"
        db.commit()
        raise HTTPException(status_code=502, detail="Mesh service did not return an export path")

    download_url = f"/mesh-assets/{quote(export_path, safe='/')}"
    export_record.status = "completed"
    export_record.download_url = download_url
    db.commit()
    return api_response(
        status="success",
        message=f"Mesh exported as {format.upper()}.",
        data={"job_id": str(export_record.id), "export_job_id": export_record.id, "format": format.upper(), "status": "Completed", "download_url": download_url, "export": result}
    )

@router.get("/export/{job_id}/status")
def get_export_status(job_id: str, db: Session = Depends(get_db)):
    try:
        export_id = int(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Export job not found") from exc

    export_job = db.query(ExportJob).filter(ExportJob.id == export_id).first()
    if not export_job:
        raise HTTPException(status_code=404, detail="Export job not found")

    return api_response(
        status="success",
        message="Job status retrieved",
        data={
            "job_id": str(export_job.id),
            "project_id": export_job.project_id,
            "format": export_job.export_format,
            "status": export_job.status,
            "download_url": export_job.download_url,
        }
    )
