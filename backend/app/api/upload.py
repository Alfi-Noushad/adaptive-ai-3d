from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.models.entities import Project, Image, User
from app.storage.file_storage import save_uploaded_image
from app.jobs.queue import create_job, dispatch_job
from app.core.response import api_response

router = APIRouter(tags=["Upload & Ingestion"])

@router.post("/upload")
def upload_image_pipeline(
    file: UploadFile = File(...),
    title: Optional[str] = Form("Untitled Mesh Project"),
    user_id: Optional[int] = Form(1),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = db.query(User).first()
        if not user:
            user = User(email="demo@meshgen.local", hashed_password="demopasswordhash", role="user")
            db.add(user)
            db.commit()
            db.refresh(user)

    saved_meta = save_uploaded_image(file)

    project = Project(
        user_id=user.id,
        title=title,
        status="processing"
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    image_record = Image(
        project_id=project.id,
        filename=saved_meta["filename"],
        storage_path=saved_meta["storage_path"],
        format=saved_meta["format"],
        file_size_bytes=saved_meta["file_size_bytes"]
    )
    db.add(image_record)
    db.commit()
    db.refresh(image_record)

    job_id = create_job("image_reconstruction", {"project_id": project.id, "image_id": image_record.id})
    dispatch_job(job_id)

    return api_response(
        status="success",
        message="Image ingested successfully. Reconstruction job queued.",
        data={
            "project_id": project.id,
            "image_id": image_record.id,
            "job_id": job_id,
            "status": "Queued",
            "file": {
                "filename": image_record.filename,
                "format": image_record.format,
                "bytes": image_record.file_size_bytes
            }
        }
    )
