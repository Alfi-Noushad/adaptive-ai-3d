import numpy as np
import open3d as o3d
import trimesh

src = trimesh.load(o3d.data.KnotMesh().path, force="mesh", process=False)
v, f = src.vertices.copy(), src.faces.copy()

# 1. Holes: delete 30 faces
f = np.delete(f, range(100, 130), axis=0)

# 2. Flipped normals: reverse winding on 50 faces
f[300:350] = f[300:350][:, ::-1]

# 3. Duplicate vertices: append copies of 20 existing vertices
v = np.vstack([v, v[:20]])

# 4. Self-intersection: small box straddling the surface
box1 = trimesh.creation.box(extents=(15, 15, 15))
box1.apply_translation(src.vertices[0])
f = np.vstack([f, box1.faces + len(v)])
v = np.vstack([v, box1.vertices])

# 5. Floating geometry: tiny box far from the knot
box2 = trimesh.creation.box(extents=(3, 3, 3))
box2.apply_translation(src.bounds[1] + 100)
f = np.vstack([f, box2.faces + len(v)])
v = np.vstack([v, box2.vertices])

trimesh.Trimesh(v, f, process=False).export("storage/broken_knot.ply")
print("Wrote storage/broken_knot.ply")