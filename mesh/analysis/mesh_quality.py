# imports
import trimesh
import numpy as np


def evaluate_mesh_quality(path: str) -> dict:
    """
    Task 3 — Mesh Quality Evaluation (deep geometric/topological pass).
    Distinct from Task 2 (descriptive analysis) and from the AI layer's
    lightweight reconstruction-confidence scoring (Master Integration
    Contract §7). Produces numerical quality scores used to drive
    repair/optimization decisions downstream (Task 5/6).
    Full defect enumeration (hole locations, self-intersections list,
    etc.) is Task 4's job — this task scores severity, not full detail.
    """

    mesh = trimesh.load(path, force="mesh")
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))

    # -------------------------
    # Raw signals
    # -------------------------
    is_watertight = bool(mesh.is_watertight)
    components = len(mesh.split(only_watertight=False))

    edges_sorted = np.sort(mesh.edges, axis=1)
    structured = np.ascontiguousarray(edges_sorted).view(
        [("", edges_sorted.dtype)] * edges_sorted.shape[1]
    )
    _, edge_counts = np.unique(structured, return_counts=True)

    boundary_edge_count = int(np.sum(edge_counts == 1))
    non_manifold_edge_count = int(np.sum(edge_counts > 2))

    # Duplicate vertices
    unique_vertices = trimesh.grouping.unique_rows(mesh.vertices)[0]
    duplicate_vertex_count = len(mesh.vertices) - len(unique_vertices)

    # Degenerate faces (zero-area triangles)
    degenerate_face_count = int(np.sum(mesh.area_faces < 1e-8))

    total_faces = max(len(mesh.faces), 1)
    total_vertices = max(len(mesh.vertices), 1)

    # -------------------------
    # Scores (0.0 - 1.0, higher = better)
    # -------------------------
    topology_score = 1.0 - min(
        (boundary_edge_count + non_manifold_edge_count) / total_faces, 1.0
    )

    geometry_score = 1.0 - min(
        (duplicate_vertex_count + degenerate_face_count) / total_vertices, 1.0
    )

    completeness_score = 1.0
    if not is_watertight:
        completeness_score -= 0.5
    if components > 1:
        completeness_score -= min(0.1 * (components - 1), 0.4)
    completeness_score = max(completeness_score, 0.0)

    overall_score = round(
        (topology_score + geometry_score + completeness_score) / 3, 3
    )

    return {
        "scores": {
            "overall": overall_score,
            "topology": round(topology_score, 3),
            "geometry": round(geometry_score, 3),
            "completeness": round(completeness_score, 3),
            "texture": None  # not assessable yet — no texture pipeline (Task 7)
        },
        "signals": {
            "watertight": is_watertight,
            "connected_components": components,
            "boundary_edges": boundary_edge_count,
            "non_manifold_edges": non_manifold_edge_count,
            "duplicate_vertices": duplicate_vertex_count,
            "degenerate_faces": degenerate_face_count
        },
        "notes": (
            "Scores are severity indicators for repair/optimization "
            "decisions (Task 5/6), not a full defect report "
            "(see Task 4 for defect enumeration)."
        )
    }