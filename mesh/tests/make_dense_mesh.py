import trimesh
import open3d as o3d

src = trimesh.load(o3d.data.KnotMesh().path, force="mesh")
v, f = trimesh.remesh.subdivide_loop(src.vertices, src.faces, iterations=3)
trimesh.Trimesh(v, f, process=False).export("storage/dense_knot.ply")
print("Wrote storage/dense_knot.ply with", len(f), "faces")