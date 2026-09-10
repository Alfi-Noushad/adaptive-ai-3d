# Adaptive AI Framework for Intelligent Multi-Model 2D-to-3D Asset Generation, Optimization and Visualization

> An AI-powered platform that converts a single 2D image into a high-quality, textured 3D model — not by relying on one fixed reconstruction model, but by intelligently analyzing each image and dynamically selecting the most suitable pretrained model through an Adaptive AI Decision Engine.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Docker](https://img.shields.io/badge/docker-compose-blue)](./docker-compose.yml)

---

## Table of Contents

- [Overview](#overview)
- [Key Contribution](#key-contribution)
- [System Pipeline](#system-pipeline)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Team](#team)
- [Project Documentation](#project-documentation)
- [Third-Party Models & Licenses](#third-party-models--licenses)
- [License](#license)

---

## Overview

Existing single-image-to-3D systems typically route every input through one fixed pretrained reconstruction model, regardless of the image's category, quality, or complexity. This project instead builds an **orchestration layer** around multiple pretrained models: it classifies the uploaded image, assesses its quality, extracts relevant features, and uses those signals to select the best-suited reconstruction model for that specific input — then automatically evaluates, repairs, and optimizes the resulting mesh before making it available for web viewing, Blender, AR, and 3D printing.

## Key Contribution

**This project does not train a new 2D-to-3D reconstruction model.** The research and engineering contribution is the **Adaptive AI Decision Engine** and the orchestration/evaluation pipeline built around existing pretrained models — intelligent model selection, automated mesh evaluation, self-healing repair, confidence prediction, and explainable AI reasoning for every decision made.

## System Pipeline

```
User Upload
   │
   ▼
Image Classification → Quality Assessment → Feature Extraction
   │
   ▼
Adaptive AI Decision Engine → Multi-Model Selection
   │
   ▼
3D Mesh Generation
   │
   ▼
Reconstruction Confidence Evaluation (AI layer) ──┐
   │                                               │
   ▼                                               │
Mesh Quality Evaluation (Mesh layer)                │
   │                                               │
   ▼                                               │
Failure Detection → Self-Healing Repair → Optimization
   │
   ▼
Texture Recommendation → Prompt-Based Editing
   │
   ▼
Database Storage
   │
   ▼
Interactive Web Viewer ──┬── Blender Export
                          ├── AR Visualization
                          └── 3D Printing Export
```

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS, React Three Fiber, Three.js, Zustand, Framer Motion |
| Backend | Python, FastAPI, PostgreSQL, Redis, SQLAlchemy, JWT |
| AI | PyTorch, Transformers, OpenCV, HuggingFace |
| Mesh Processing | Open3D, Trimesh, PyMeshLab, Blender Python API |
| Deployment | Docker, Docker Compose, GitHub Actions |

## Project Structure

```
adaptive-ai-3d/
├── frontend/       # React + TypeScript client
├── backend/        # FastAPI service — auth, DB, orchestration between layers
├── ai/             # Classification, quality assessment, decision engine, model selection
├── mesh/           # Mesh analysis, repair, optimization, texture, Blender/AR/print export
├── database/       # Schema, migrations
├── docs/           # SRS, SDD, Master Integration Contract, review roadmap
├── docker/         # Per-service Dockerfiles
├── tests/          # Cross-service integration tests
├── scripts/        # Dev/setup utility scripts
├── .github/        # CI/CD workflows
├── docker-compose.yml
├── .env.example
└── LICENSE
```

All cross-service communication (schemas, endpoints, response format) is governed by [`docs/00-MASTER-INTEGRATION-CONTRACT.md`](./docs/00-MASTER-INTEGRATION-CONTRACT.md) — this is the single source of truth if any service's behavior seems to disagree with another.

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend dev outside Docker)
- Python 3.11+ (for local backend/AI/mesh dev outside Docker)
- (AI service only) NVIDIA GPU + CUDA, recommended 8GB+ VRAM for running reconstruction models

### Quick Start (Docker)

```bash
git clone https://github.com/<org-or-username>/adaptive-ai-3d.git
cd adaptive-ai-3d
cp .env.example .env      # fill in required values
docker compose up --build
```

This brings up: frontend, backend, AI service, mesh service, PostgreSQL, and Redis.

| Service | Default URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

### Local Development (without Docker)

```bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# AI service
cd ai && pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Mesh service
cd mesh && pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

## Environment Variables

See [`.env.example`](./.env.example) for the full list. Key variables:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `JWT_SECRET_KEY` | Secret for signing auth tokens |
| `AI_SERVICE_URL` | Internal URL the backend uses to reach the AI layer |
| `MESH_SERVICE_URL` | Internal URL the backend uses to reach the mesh layer |
| `STORAGE_PATH` | Local/mounted path for uploaded images and generated assets |

Never commit `.env` — only `.env.example` with placeholder values.

## API Documentation

Full interactive API docs are auto-generated by FastAPI and available at `/docs` (Swagger UI) and `/redoc` once the backend is running. The canonical endpoint contracts (Frontend↔Backend, Backend↔AI, Backend↔Mesh) are documented in [`docs/00-MASTER-INTEGRATION-CONTRACT.md`](./docs/00-MASTER-INTEGRATION-CONTRACT.md).

## Testing

```bash
# Backend
cd backend && pytest

# AI service
cd ai && pytest

# Mesh service
cd mesh && pytest

# Frontend
cd frontend && npm test

# Full integration suite (requires all services running)
cd tests && pytest integration/
```

## Team

| Name | Role | GitHub |
|---|---|---|
| Manav Rai | Frontend Lead | @manavrai-as |
| Swagath BL | Backend Lead | @swagath20 |
| Vishnu G Nair | AI Layer Lead | @Maidenless200 |
| Alfi Nousahd | Mesh/3D Processing Lead | @Alfi-Noushad |

## Project Documentation

- [Software Requirements Specification (SRS)](./docs/SRS.pdf)
- [Software Design Document (SDD)](./docs/SDD.pdf)
- [Master Integration Contract](./docs/00-MASTER-INTEGRATION-CONTRACT.md)
- [8-Review Project Roadmap](./docs/06-8-REVIEW-ROADMAP.pdf)

## Third-Party Models & Licenses

This project integrates pretrained open-source 2D-to-3D reconstruction models rather than training new ones. Each model retains its own original license — see [`THIRD_PARTY_LICENSES.md`](./THIRD_PARTY_LICENSES.md) for the full list and terms.

## License

This project is licensed under the MIT License — see [`LICENSE`](./LICENSE) for details.

Note: the MIT License applies to code written by this team. Integrated third-party pretrained models are governed by their own respective licenses (see above).
