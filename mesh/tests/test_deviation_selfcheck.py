import trimesh
from mesh.optimizer.mesh_optimizer import _deviation

m = trimesh.load("storage/dense_knot.ply", force="mesh")
print("self-comparison:", _deviation(m, m.copy()))