import json
from mesh.exports.exporter import export_mesh

print(json.dumps(
    export_mesh("storage/dense_knot_optimized.ply", "storage/dense_knot_optimized.glb", "glb"),
    indent=2,
))