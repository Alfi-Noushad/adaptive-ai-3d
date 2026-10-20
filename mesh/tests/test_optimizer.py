import json
from mesh.optimizer.mesh_optimizer import optimize_mesh

for name in ("dense_knot.ply", "knot.ply"):
    print(f"\n===== {name} =====")
    out = f"storage/{name.replace('.ply', '_optimized.ply')}"
    print(json.dumps(optimize_mesh(f"storage/{name}", out), indent=2))