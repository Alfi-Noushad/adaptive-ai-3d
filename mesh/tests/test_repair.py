import json
from mesh.repair.self_healing import repair_mesh

for name in ("broken_knot.ply", "knot.ply"):
    print(f"\n===== {name} =====")
    out = f"storage/{name.replace('.ply', '_repaired.ply')}"
    print(json.dumps(repair_mesh(f"storage/{name}", out), indent=2))