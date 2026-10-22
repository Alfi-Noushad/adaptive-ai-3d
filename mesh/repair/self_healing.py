import numpy as np
import pymeshlab
import trimesh

from mesh.analysis.failure_detection import detect_failures, FLOATING_FACE_RATIO

MAX_HOLE_EDGES = 200  # holes with more boundary edges than this are left open


def _close_holes(mesh: trimesh.Trimesh, max_hole_edges: int) -> trimesh.Trimesh:
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(
        vertex_matrix=np.asarray(mesh.vertices, dtype=np.float64),
        face_matrix=np.asarray(mesh.faces, dtype=np.int32),
    ))
    ms.meshing_close_holes(maxholesize=max_hole_edges)
    m = ms.current_mesh()
    return trimesh.Trimesh(m.vertex_matrix(), m.face_matrix(), process=False)


def repair_mesh(path: str, output_path: str, max_hole_edges: int = MAX_HOLE_EDGES) -> dict:
    """Task 5: repair defects, save the result, verify with Task 4's detector."""
    before = detect_failures(path)
    mesh = trimesh.load(path, force="mesh", process=False)
    actions = []

    def log(action: str, detail: str):
        actions.append({"action": action, "detail": detail})

    faces_start = len(mesh.faces)

    # 1. Duplicate vertices
    v0 = len(mesh.vertices)
    mesh.merge_vertices()
    if len(mesh.vertices) < v0:
        log("merge_vertices", f"merged {v0 - len(mesh.vertices)} duplicate vertices")

    # 2. Degenerate and duplicate faces
    f0 = len(mesh.faces)
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.update_faces(mesh.unique_faces())
    if len(mesh.faces) < f0:
        log("remove_bad_faces", f"removed {f0 - len(mesh.faces)} degenerate/duplicate faces")

    # 3. Floating geometry: keep every substantial component, drop tiny ones
    parts = mesh.split(only_watertight=False)
    largest = max(parts, key=lambda p: len(p.faces))
    reference_bounds = largest.bounds.copy()  # for the shape-drift check
    keep = [p for p in parts if len(p.faces) >= FLOATING_FACE_RATIO * len(largest.faces)]
    if len(keep) < len(parts):
        mesh = keep[0] if len(keep) == 1 else trimesh.util.concatenate(keep)
        log("remove_floating", f"removed {len(parts) - len(keep)} floating components")

    # 4. Winding, then holes, then orientation again (closed mesh can be checked for inversion)
    trimesh.repair.fix_winding(mesh)

    e0 = len(mesh.faces)
    mesh = _close_holes(mesh, max_hole_edges)
    if len(mesh.faces) > e0:
        log("close_holes", f"added {len(mesh.faces) - e0} faces (max hole size {max_hole_edges} edges)")

    trimesh.repair.fix_normals(mesh)
    log("fix_normals", "made winding consistent and normals outward")

    mesh.remove_unreferenced_vertices()
    mesh.export(output_path)

    # Verify on the actual saved file
    after = detect_failures(output_path)

    diag = float(np.linalg.norm(reference_bounds[1] - reference_bounds[0]))
    drift = float(np.max(np.abs(mesh.bounds - reference_bounds)) / diag) if diag else 0.0

    return {
        "actions": actions,
        "before": before["summary"],
        "after": after["summary"],
        "unresolved": after["summary"]["found"],
        "faces": {"before": int(faces_start), "after": int(len(mesh.faces))},
        "shape_check": {
            "bounds_drift_ratio": round(drift, 5),
            "note": "max bounding-box change relative to the main body's diagonal",
        },
    }