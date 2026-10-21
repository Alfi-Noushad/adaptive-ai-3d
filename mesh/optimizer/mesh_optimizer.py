import time

import numpy as np
import pymeshlab
import trimesh



SUBDIVIDE_BELOW = 2_000
DECIMATE_ABOVE = 20_000
DEVIATION_SAMPLES = 20_000


def _adaptive_target(n_faces: int) -> int:
    if n_faces > 500_000:
        return 100_000
    if n_faces > 100_000:
        return int(n_faces * 0.4)
    if n_faces > DECIMATE_ABOVE:
        return int(n_faces * 0.5)
    return n_faces


def _decimate(mesh: trimesh.Trimesh, target_faces: int) -> trimesh.Trimesh:
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(
        vertex_matrix=np.asarray(mesh.vertices, dtype=np.float64),
        face_matrix=np.asarray(mesh.faces, dtype=np.int32),
    ))
    ms.meshing_decimation_quadric_edge_collapse(
        targetfacenum=target_faces,
        preserveboundary=True,
        preservenormal=True,
        preservetopology=True,
        optimalplacement=True,
        planarquadric=True,
    )
    m = ms.current_mesh()
    return trimesh.Trimesh(m.vertex_matrix(), m.face_matrix(), process=False)


def _deviation(original: trimesh.Trimesh, optimized: trimesh.Trimesh) -> dict:
    """Two-way vertex-to-surface distance (Hausdorff), relative to bbox diagonal."""
    ms = pymeshlab.MeshSet()
    for m in (original, optimized):
        ms.add_mesh(pymeshlab.Mesh(
            vertex_matrix=np.asarray(m.vertices, dtype=np.float64),
            face_matrix=np.asarray(m.faces, dtype=np.int32),
        ))
    a = ms.get_hausdorff_distance(sampledmesh=1, targetmesh=0, samplevert=True,
                                  sampleedge=False, sampleface=False)
    b = ms.get_hausdorff_distance(sampledmesh=0, targetmesh=1, samplevert=True,
                                  sampleedge=False, sampleface=False)
    diag = float(np.linalg.norm(original.bounds[1] - original.bounds[0]))
    return {
        "mean_ratio": round(float(max(a["mean"], b["mean"]) / diag), 6),
        "max_ratio": round(float(max(a["max"], b["max"]) / diag), 6),
        "note": "two-way vertex-to-surface distance relative to bounding-box diagonal",
    }

def optimize_mesh(path: str, output_path: str,
                  target_faces: int | None = None,
                  smooth: bool = False) -> dict:
    """Task 6: adaptive decimation / subdivision, saved as a new version."""
    t0 = time.perf_counter()
    original = trimesh.load(path, force="mesh")
    mesh = original.copy()
    n0 = len(mesh.faces)
    actions = []

    if target_faces is None and n0 < SUBDIVIDE_BELOW:
        v, f = trimesh.remesh.subdivide_loop(mesh.vertices, mesh.faces, iterations=1)
        mesh = trimesh.Trimesh(v, f, process=False)
        actions.append({"action": "subdivide_loop",
                        "detail": f"{n0} faces is low, one subdivision pass"})
    else:
        target = target_faces or _adaptive_target(n0)
        if target < n0:
            mesh = _decimate(mesh, target)
            actions.append({"action": "decimate_quadric",
                            "detail": f"target {target} faces (from {n0})"})
        else:
            actions.append({"action": "skip_decimation",
                            "detail": f"{n0} faces is already at or under target"})

    if smooth:
        trimesh.smoothing.filter_taubin(mesh, iterations=10)
        actions.append({"action": "smooth_taubin", "detail": "10 iterations"})

    mesh.remove_unreferenced_vertices()
    mesh.export(output_path)

    changed = len(mesh.faces) != n0 or smooth
    return {
        "actions": actions,
        "faces": {
            "before": int(n0),
            "after": int(len(mesh.faces)),
            "reduction_pct": round(100 * (1 - len(mesh.faces) / n0), 2),
        },
        "watertight": {"before": bool(original.is_watertight),
                       "after": bool(mesh.is_watertight)},
        "deviation": _deviation(original, mesh) if changed else None,
        "elapsed_seconds": round(time.perf_counter() - t0, 3),
    }