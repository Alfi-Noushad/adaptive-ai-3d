from mesh.scripts.mesh_analyasis import analyze_mesh

@router.post("/analyze")
def analyze(path: str):
    try:
        data = analyze_mesh(path)

        return {
            "status": "success",
            "message": "Mesh analyzed successfully",
            "data": data,
            "error": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": "Mesh analysis failed",
            "data": None,
            "error": {
                "type": type(exc).__name__,
                "message": str(exc)
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }