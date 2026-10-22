import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

from app.database.session import SessionLocal
from app.models.entities import Project, GeneratedMesh, AIEvaluationReport, MeshQualityReport
from app.services.ai_client import ai_client
from app.services.mesh_client import mesh_client

executor = ThreadPoolExecutor(max_workers=3)
_JOB_REGISTRY: Dict[str, Dict[str, Any]] = {}

def create_job(job_type: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    job_id = str(uuid.uuid4())
    _JOB_REGISTRY[job_id] = {
        "job_id": job_id,
        "job_type": job_type,
        "status": "Queued",
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": None,
        "error": None
    }
    return job_id

def get_job_status(job_id: str) -> Optional[Dict[str, Any]]:
    return _JOB_REGISTRY.get(job_id)

def _execute_pipeline_sync(job_id: str, project_id: int, image_path: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_pipeline_orchestration(job_id, project_id, image_path))
    finally:
        loop.close()

async def _pipeline_orchestration(job_id: str, project_id: int, image_path: str):
    if job_id not in _JOB_REGISTRY:
        return

    _JOB_REGISTRY[job_id]["status"] = "Running"
    _JOB_REGISTRY[job_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

    db = SessionLocal()
    try:
        # 1. AI Layer: Classification & Selection
        ai_res = await ai_client.classify_and_select(image_path)
        ai_rep = AIEvaluationReport(
            project_id=project_id,
            classification=ai_res.get("classification"),
            quality_score=ai_res.get("quality_score"),
            selected_model=ai_res.get("selected_model"),
            reasoning_xai=ai_res.get("reasoning_xai"),
            confidence_scores=ai_res.get("confidence_scores")
        )
        db.add(ai_rep)

        # 2. Track Generated Mesh
        mesh_record = GeneratedMesh(
            project_id=project_id,
            mesh_type="initial",
            storage_path=f"storage/meshes/model_{project_id}.obj",
            vertex_count=28450,
            face_count=56000
        )
        db.add(mesh_record)

        # 3. Mesh Layer: Evaluation & Topology Repair
        mesh_res = await mesh_client.evaluate_and_repair(mesh_record.storage_path)
        mesh_rep = MeshQualityReport(
            project_id=project_id,
            topology_grade=mesh_res.get("topology_grade"),
            defect_list=mesh_res.get("defect_list"),
            repair_actions_taken=mesh_res.get("repair_actions_taken"),
            optimization_stats=mesh_res.get("optimization_stats")
        )
        db.add(mesh_rep)

        # 4. Update Project Status to Completed
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.status = "completed"

        db.commit()

        # 5. Complete Job
        _JOB_REGISTRY[job_id]["status"] = "Completed"
        _JOB_REGISTRY[job_id]["result"] = {
            "project_id": project_id,
            "selected_model": ai_res.get("selected_model"),
            "topology_grade": mesh_res.get("topology_grade"),
            "status": "ready"
        }
    except Exception as e:
        db.rollback()
        _JOB_REGISTRY[job_id]["status"] = "Failed"
        _JOB_REGISTRY[job_id]["error"] = str(e)
    finally:
        db.close()
        _JOB_REGISTRY[job_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

def dispatch_pipeline(job_id: str, project_id: int, image_path: str):
    executor.submit(_execute_pipeline_sync, job_id, project_id, image_path)
