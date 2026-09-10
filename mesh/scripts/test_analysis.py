import open3d as o3d
from mesh.scripts.mesh_analyasis import analyze_mesh

dataset = o3d.data.KnotMesh()
obj_path = dataset.path

print("Testing:", obj_path)

result = analyze_mesh(obj_path)

print("\n===== MESH ANALYSIS =====")
print(result)