import json
from mesh.analysis.failure_detection import detect_failures

for name in ("knot.ply", "broken_knot.ply"):
    print(f"\n===== {name} =====")
    print(json.dumps(detect_failures(f"storage/{name}"), indent=2))