import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.session import engine, Base
import app.models.entities
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.analyze import router as analyze_router
from app.api.upload import router as upload_router
from app.api.projects import router as projects_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Adaptive AI Framework for Intelligent Multi-Model 2D-to-3D Asset Generation, Optimization and Visualization",
    description="Backend service for 2D image ingestion, 3D mesh generation, and quality evaluation.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(projects_router)
app.include_router(analyze_router)

# Mesh and backend containers share this directory through the compose volume.
# Locally it resolves to the repository's storage directory, also used by Mesh.
mesh_storage_root = Path(
    os.getenv("MESH_STORAGE_ROOT", str(Path(__file__).resolve().parents[2] / "storage"))
).resolve()
mesh_storage_root.mkdir(parents=True, exist_ok=True)
app.mount("/mesh-assets", StaticFiles(directory=str(mesh_storage_root)), name="mesh-assets")
