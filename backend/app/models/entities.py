from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.database.session import Base

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), default="Untitled Mesh Project")
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="projects")
    image = relationship("Image", back_populates="project", uselist=False, cascade="all, delete-orphan")
    generated_meshes = relationship("GeneratedMesh", back_populates="project", cascade="all, delete-orphan")
    ai_evaluation_report = relationship("AIEvaluationReport", back_populates="project", uselist=False, cascade="all, delete-orphan")
    mesh_quality_report = relationship("MeshQualityReport", back_populates="project", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="project", cascade="all, delete-orphan")
    prompt_edits = relationship("PromptEdit", back_populates="project", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="project", cascade="all, delete-orphan")
    history_entries = relationship("History", back_populates="project", cascade="all, delete-orphan")
    export_jobs = relationship("ExportJob", back_populates="project", cascade="all, delete-orphan")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True, nullable=False)
    filename = Column(String(255), nullable=False)
    storage_path = Column(String(500), nullable=False)
    format = Column(String(50), nullable=False)
    resolution = Column(String(50), nullable=True)
    file_size_bytes = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="image")


class ReconstructionModel(Base):
    __tablename__ = "reconstruction_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # e.g., Wonder3D, TripoSR, Stable Fast 3D
    version = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    metadata_info = Column(JSON, nullable=True)

    generated_meshes = relationship("GeneratedMesh", back_populates="reconstruction_model")


class GeneratedMesh(Base):
    __tablename__ = "generated_meshes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("reconstruction_models.id"), nullable=True)
    mesh_type = Column(String(50), nullable=False)  # initial, optimized
    version = Column(Integer, default=1)
    storage_path = Column(String(500), nullable=False)
    vertex_count = Column(Integer, nullable=True)
    face_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="generated_meshes")
    reconstruction_model = relationship("ReconstructionModel", back_populates="generated_meshes")


class AIEvaluationReport(Base):
    __tablename__ = "ai_evaluation_reports"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True, nullable=False)
    classification = Column(String(100), nullable=True)
    quality_score = Column(Float, nullable=True)
    selected_model = Column(String(100), nullable=True)
    reasoning_xai = Column(Text, nullable=True)
    confidence_scores = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="ai_evaluation_report")


class MeshQualityReport(Base):
    __tablename__ = "mesh_quality_reports"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True, nullable=False)
    topology_grade = Column(String(20), nullable=True)
    defect_list = Column(JSON, nullable=True)
    repair_actions_taken = Column(JSON, nullable=True)
    optimization_stats = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="mesh_quality_report")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category = Column(String(100), nullable=False)  # texture, material, pipeline
    suggestion_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="recommendations")


class PromptEdit(Base):
    __tablename__ = "prompt_edits"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    prompt_text = Column(Text, nullable=False)
    edit_status = Column(String(50), default="queued")  # queued, applying, completed, failed
    result_mesh_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="prompt_edits")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="feedback")
    user = relationship("User", back_populates="feedback")


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    action_type = Column(String(100), nullable=False)
    summary_snapshot = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="history_entries")


class ExportJob(Base):
    __tablename__ = "export_jobs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    export_format = Column(String(20), nullable=False)  # OBJ, GLB, FBX, PLY, STL, BLENDER
    status = Column(String(50), default="pending")      # pending, running, completed, failed
    download_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="export_jobs")


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # INFO, WARNING, ERROR
    source = Column(String(100), nullable=False)  # API, AI, MESH, EXPORT
    message = Column(Text, nullable=False)
    context_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=utc_now)