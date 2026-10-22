import trimesh

# Adding a format later = add its extension here (Review 6, Task 12)
SUPPORTED_FORMATS = {"glb"}


def export_mesh(path: str, output_path: str, fmt: str) -> dict:
    """Export a mesh to a downloadable format and verify the saved file."""
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format '{fmt}'. Supported: {sorted(SUPPORTED_FORMATS)}")

    mesh = trimesh.load(path, force="mesh")
    mesh.export(output_path, file_type=fmt)

    # Verify on the saved file, not on trust
    check = trimesh.load(output_path, force="mesh")
    faces_ok = len(check.faces) == len(mesh.faces)

    import os
    return {
        "format": fmt,
        "size_bytes": os.path.getsize(output_path),
        "faces": int(len(check.faces)),
        "verified": bool(faces_ok),
    }