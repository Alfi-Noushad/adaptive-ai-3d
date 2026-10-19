import uuid
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

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

def _simulate_reconstruction_worker(job_id: str):
    if job_id not in _JOB_REGISTRY:
        return
    _JOB_REGISTRY[job_id]["status"] = "Running"
    _JOB_REGISTRY[job_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

    time.sleep(2)

    _JOB_REGISTRY[job_id]["status"] = "Completed"
    _JOB_REGISTRY[job_id]["result"] = {"reconstruction": "ready", "mesh_id": 1}
    _JOB_REGISTRY[job_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

def dispatch_job(job_id: str):
    executor.submit(_simulate_reconstruction_worker, job_id)
