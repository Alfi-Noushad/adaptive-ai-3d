import open3d as o3d
import trimesh
import pymeshlab


def analyze_mesh(path: str) -> dict:
    # -------------------------
    # Open3D
    # -------------------------
    o3d_mesh = o3d.io.read_triangle_mesh(path)
    o3d_mesh.compute_vertex_normals()

    # -------------------------
    # Trimesh
    # -------------------------
    mesh = trimesh.load(path, force="mesh")

    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(
            tuple(mesh.geometry.values())
        )

    # -------------------------
    # PyMeshLab
    # -------------------------
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(path)
    pml_mesh = ms.current_mesh()

    # -------------------------
    # Geometry
    # -------------------------
    bounds = mesh.bounds
    size = bounds[1] - bounds[0]

    # -------------------------
    # Topology
    # -------------------------
    components = mesh.split(only_watertight=False)

    boundary_edges = 0
    non_manifold_edges = 0

    edge_use_count = {}

    for face in mesh.faces:
        edges = [
            tuple(sorted((face[0], face[1]))),
            tuple(sorted((face[1], face[2]))),
            tuple(sorted((face[2], face[0])))
        ]

        for edge in edges:
            edge_use_count[edge] = edge_use_count.get(edge, 0) + 1

    boundary_edges = sum(
        1 for count in edge_use_count.values()
        if count == 1
    )

    non_manifold_edges = sum(
        1 for count in edge_use_count.values()
        if count > 2
    )

    # -------------------------
    # Report
    # -------------------------
    return {
        "mesh": {
            "vertices": int(pml_mesh.vertex_number()),
            "faces": int(pml_mesh.face_number()),
            "triangles": int(len(mesh.faces)),
            "polygons": int(pml_mesh.face_number())
        },

        "normals": {
            "has_vertex_normals": bool(
                o3d_mesh.has_vertex_normals()
            ),
            "vertex_normals": int(len(o3d_mesh.vertex_normals)),
            "face_normals": int(len(mesh.face_normals))
        },

        "topology": {
            "watertight": bool(mesh.is_watertight),
            "boundary_edges": int(boundary_edges),
            "non_manifold_edges": int(non_manifold_edges),
            "connected_components": int(len(components))
        },

        "geometry": {
            "bounding_box": {
                "min": bounds[0].tolist(),
                "max": bounds[1].tolist(),
                "size": size.tolist()
            },
            "surface_area": float(mesh.area),
            "volume": float(mesh.volume)
        }
    }