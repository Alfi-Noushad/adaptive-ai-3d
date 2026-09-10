from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.auth import router as auth_router

app = FastAPI(
    title="2D to 3D Mesh Converter API",
    description="Backend service for 2D image ingestion, 3D mesh generation, and quality evaluation.",
    version="0.1.0"
)

# CORS configuration to allow frontend clients to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any frontend port (e.g., Vite :5173, React :3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health_router)
app.include_router(auth_router)