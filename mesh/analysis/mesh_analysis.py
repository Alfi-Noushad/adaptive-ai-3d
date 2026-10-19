# imports
# Using only Trimesh for now will use other libraries when needed
import trimesh


def analyze_mesh(path: str) -> dict:
    """
    Task 2 — Mesh Analysis.
    Purely descriptive/structural report: vertices, faces, triangles,
    normals, topology, bounding box, surface area, volume, polygon count.
    No defect detection here (holes, non-manifold edges, etc. belong to
    Task 3/4 — Mesh Quality Evaluation / Failure Detection).
    """

    # -------------------------
    # Load
    # -------------------------
    mesh = trimesh.load(path, force="mesh")

    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(
            tuple(mesh.geometry.values())
        )

    # -------------------------
    # Geometry
    # -------------------------
    bounds = mesh.bounds
    size = bounds[1] - bounds[0]

    # -------------------------
    # Topology (structural facts only — not defect analysis)
    # -------------------------
    is_watertight = bool(mesh.is_watertight)
    connected_components = len(mesh.split(only_watertight=False))

    # -------------------------
    # Volume is only meaningful for watertight meshes.
    # Report None rather than a misleading number.
    # -------------------------
    volume = float(mesh.volume) if is_watertight else None

    # -------------------------
    # Report
    # -------------------------
    return {
        "mesh": {
            "vertices": int(len(mesh.vertices)),
            "faces": int(len(mesh.faces)),
            "triangles": int(len(mesh.faces)),  # Trimesh faces are triangles after force="mesh"
            "polygons": int(len(mesh.faces))
        },

        "normals": {
            "has_vertex_normals": mesh.vertex_normals is not None,
            "vertex_normals": int(len(mesh.vertex_normals)),
            "face_normals": int(len(mesh.face_normals))
        },

        "topology": {
            "watertight": is_watertight,
            "connected_components": int(connected_components)
        },

        "geometry": {
            "bounding_box": {
                "min": bounds[0].tolist(),
                "max": bounds[1].tolist(),
                "size": size.tolist()
            },
            "surface_area": float(mesh.area),
            "volume": volume
        }
    }