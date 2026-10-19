import numpy as np
import pymeshlab
import trimesh

DEGENERATE_AREA = 1e-8
FLOATING_FACE_RATIO = 0.01  # component under 1% of the largest = "floating"

SEVERITY = {
    "non_manifold_edges": "critical",
    "self_intersections": "critical",
    "inverted_volume": "critical",
    "holes": "major",
    "inconsistent_winding": "major",
    "floating_geometry": "major",
    "disconnected_components": "minor",
    "duplicate_vertices": "minor",
    "degenerate_faces": "minor",
}


def _count_self_intersections(mesh: trimesh.Trimesh):
    """Faces intersecting other faces, via PyMeshLab. None if it can't run."""
    try:
        ms = pymeshlab.MeshSet()
        ms.add_mesh(pymeshlab.Mesh(
            vertex_matrix=np.asarray(mesh.vertices, dtype=np.float64),
            face_matrix=np.asarray(mesh.faces, dtype=np.int32),
        ))
        ms.compute_selection_by_self_intersections_per_face()
        return int(ms.current_mesh().selected_face_number())
    except Exception:
        return None


def _entry(name, count):
    return {
        "count": count,
        "detected": bool(count) if count is not None else None,
        "severity": SEVERITY[name],
    }


def detect_failures(path: str) -> dict:
    """Task 4: enumerate defects. Detection only, repair is Task 5."""
    raw = trimesh.load(path, force="mesh", process=False)

    # Duplicates must be counted on the raw data, before any merging
    duplicate_vertices = len(raw.vertices) - len(np.unique(raw.vertices, axis=0))

    # Everything else runs on a merged copy so seams don't look like holes
    mesh = raw.copy()
    mesh.merge_vertices()

    # Edge usage: 1 = boundary (hole edge), 2 = healthy, >2 = non-manifold
    edges = np.sort(mesh.edges, axis=1)
    unique_edges, counts = np.unique(edges, axis=0, return_counts=True)
    boundary_edges = unique_edges[counts == 1]
    non_manifold_edges = int(np.sum(counts > 2))

    # Holes = connected loops of boundary edges
    hole_loops = 0
    if len(boundary_edges):
        hole_loops = len(trimesh.graph.connected_components(boundary_edges))

    # Components: split off small pieces as "floating"
    parts = mesh.split(only_watertight=False)
    face_counts = [len(p.faces) for p in parts]
    largest = max(face_counts) if face_counts else 0
    floating = sum(1 for c in face_counts if c < FLOATING_FACE_RATIO * largest)

    degenerate = int(np.sum(mesh.area_faces < DEGENERATE_AREA))

    # Orientation: mixed winding, or a closed mesh whose normals all point inward
    inconsistent_winding = 0 if mesh.is_winding_consistent else 1
    inverted_volume = 1 if (mesh.is_watertight and mesh.volume < 0) else 0

    defects = {
        "holes": _entry("holes", hole_loops),
        "non_manifold_edges": _entry("non_manifold_edges", non_manifold_edges),
        "floating_geometry": _entry("floating_geometry", floating),
        "disconnected_components": _entry("disconnected_components", max(len(parts) - 1, 0)),
        "duplicate_vertices": _entry("duplicate_vertices", int(duplicate_vertices)),
        "degenerate_faces": _entry("degenerate_faces", degenerate),
        "inconsistent_winding": _entry("inconsistent_winding", inconsistent_winding),
        "inverted_volume": _entry("inverted_volume", inverted_volume),
        "self_intersections": _entry("self_intersections", _count_self_intersections(mesh)),
    }

    found = [k for k, v in defects.items() if v["detected"]]
    return {
        "summary": {
            "defect_types_found": len(found),
            "found": found,
            "has_critical": any(defects[k]["severity"] == "critical" for k in found),
        },
        "defects": defects,
    }