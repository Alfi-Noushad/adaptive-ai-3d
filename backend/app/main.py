from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(
    title="2D to 3D Mesh Converter API",
    description="Backend service for 2D image ingestion, 3D mesh generation, and quality evaluation.",
    version="0.1.0"
)

app.include_router(health_router)