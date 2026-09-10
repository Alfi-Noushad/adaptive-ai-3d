import sys
from pathlib import Path
from datetime import datetime, timezone
import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException, status

# Ensure the root adaptive-ai-3d directory is in sys.path so mesh can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mesh.scripts.mesh_analyasis import analyze_mesh

router = APIRouter(tags=["Mesh Analysis"])


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix if file.filename else ".obj"

    # Save uploaded mesh temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
    except Exception as exc:
        return {
            "status": "error",
            "message": "Mesh upload failed",
            "data": None,
            "error": {
                "type": type(exc).__name__,
                "message": str(exc),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # Pass the temp file path directly to the teammate's analysis function
    try:
        result = analyze_mesh(tmp_path)
        return {
            "status": "success",
            "message": "Mesh analyzed successfully",
            "data": result,
            "error": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": "Mesh analysis failed",
            "data": None,
            "error": {
                "type": type(exc).__name__,
                "message": str(exc),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    finally:
        # Clean up temporary file
        file_obj = Path(tmp_path)
        if file_obj.exists():
            file_obj.unlink()