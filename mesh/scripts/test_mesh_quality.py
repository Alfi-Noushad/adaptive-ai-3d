import open3d as o3d
from mesh.scripts.mesh_quality import evaluate_mesh_quality

dataset = o3d.data.KnotMesh()
obj_path = dataset.path

print("Testing:", obj_path)

result = evaluate_mesh_quality(obj_path)

print("\n===== MESH QUALITY EVALUATION =====")
for section, values in result.items():
    print(f"\n{section}:")
    if isinstance(values, dict):
        for k, v in values.items():
            print(f"  {k}: {v}")
    else:
        print(f"  {values}")