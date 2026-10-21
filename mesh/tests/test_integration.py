import pytest
from fastapi.testclient import TestClient

from mesh.api.main import app
from mesh.utils.storage import STORAGE_ROOT

client = TestClient(app)
ENVELOPE_KEYS = {"status", "message", "data", "error", "timestamp"}


def call(endpoint: str, body: dict):
    """POST like Backend would, and enforce the Contract section 2 envelope."""
    r = client.post(endpoint, json=body)
    j = r.json()
    assert set(j.keys()) == ENVELOPE_KEYS, f"{endpoint}: envelope deviates: {sorted(j)}"
    return r.status_code, j


@pytest.fixture(scope="module")
def source():
    if not (STORAGE_ROOT / "broken_knot.ply").exists():
        pytest.skip("Run: python -m mesh.tests.make_broken_mesh")
    return "broken_knot.ply"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert set(r.json().keys()) == ENVELOPE_KEYS


def test_core_happy_path(source):
    # 1. Evaluate the raw mesh: defects must be found
    code, j = call("/evaluate", {"mesh_path": source})
    assert code == 200 and j["status"] == "success"
    assert j["data"]["defect_report"]["summary"]["defect_types_found"] > 0
    print("\n[evaluate raw] scores:", j["data"]["scores"])

    # 2. Repair
    code, j = call("/repair", {"mesh_path": source})
    assert code == 200 and j["status"] == "success"
    assert j["data"]["unresolved"] == []
    repaired = j["data"]["repaired_mesh_path"]
    print("[repair] ->", repaired)

    # 3. Re-evaluate the repaired mesh: must be clean
    code, j = call("/evaluate", {"mesh_path": repaired})
    assert j["data"]["defect_report"]["summary"]["defect_types_found"] == 0
    assert j["data"]["signals"]["watertight"] is True
    print("[evaluate repaired] scores:", j["data"]["scores"])

    # 4. Optimize (target below 2,874 faces so decimation actually runs)
    code, j = call("/optimize", {"mesh_path": repaired, "target_faces": 1500})
    assert code == 200 and j["status"] == "success"
    assert j["data"]["faces"]["after"] < j["data"]["faces"]["before"]
    optimized = j["data"]["optimized_mesh_path"]
    print("[optimize] faces:", j["data"]["faces"], "deviation:", j["data"]["deviation"])

    # 5. Export GLB
    code, j = call("/export", {"mesh_path": optimized, "format": "glb"})
    assert code == 200 and j["data"]["verified"] is True
    assert (STORAGE_ROOT / j["data"]["export_path"]).is_file()
    print("[export]", j["data"])


@pytest.mark.parametrize("endpoint", ["/analyze", "/evaluate", "/repair", "/optimize", "/export"])
def test_missing_file_returns_error_envelope(endpoint):
    code, j = call(endpoint, {"mesh_path": "does_not_exist.ply"})
    assert code == 404 and j["status"] == "error" and j["data"] == {}


def test_path_traversal_blocked():
    code, j = call("/analyze", {"mesh_path": "../README.md"})
    assert code == 400 and j["status"] == "error"


def test_bad_body_returns_error_envelope():
    code, j = call("/analyze", {})
    assert code == 422 and j["status"] == "error"


def test_unsupported_export_format():
    code, j = call("/export", {"mesh_path": "knot.ply", "format": "fbx"})
    assert code == 400 and j["status"] == "error"