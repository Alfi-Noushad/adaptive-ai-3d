"""
Task 1 — environment verification script.
Confirms Open3D, Trimesh, and PyMeshLab can each load and inspect
a sample OBJ mesh. Not part of the real pipeline — throwaway sanity check.
"""
import open3d as o3d
import trimesh
import pymeshlab

def get_sample_obj_path():
    # Open3D ships sample meshes; downloads once and caches locally.
    dataset = o3d.data.KnotMesh()
    return dataset.path

def test_open3d(path):
    print("\n---open3D----")
    mesh = o3d.io.read_triangle_mesh(path)
    print(f"Vertices: {len(mesh.vertices)}")
    print(f"Triangles: {len(mesh.triangles)}")
    print(f"Has normals: {mesh.has_vertex_normals()}")

def test_trimesh(path):
    print("\n---Trimesh---")
    mesh = trimesh.load(path)
    print(f"Vertices: {len(mesh.vertices)}")
    print(f"Faces: {len(mesh.faces)}")
    print(f"Watertight: {mesh.is_watertight}")
    print(f"Bounding box: {mesh.bounds.tolist()}")


def test_pymeshlab(path):
    print("\n -- PymeshLab---")
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(path)
    m = ms.current_mesh()
    print(f"Vertices: {m.vertex_number()}")
    print(f"Faces: {m.face_number()}")


if __name__ == "__main__":
    obj_path = get_sample_obj_path()
    print(f"Using sample mesh: {obj_path}")

    test_open3d(obj_path)
    test_trimesh(obj_path)
    test_pymeshlab(obj_path)

    print("\n All 3 libraries laoded and read the mesh successfully.")