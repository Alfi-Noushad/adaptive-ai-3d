import os
from typing import Any

import httpx


MESH_SERVICE_URL = os.getenv("MESH_SERVICE_URL", "http://127.0.0.1:8002")


class MeshServiceError(RuntimeError):
    """Raised when the Mesh layer cannot process a backend-supplied mesh."""


class MeshClient:
    def __init__(self, base_url: str = MESH_SERVICE_URL, timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}{endpoint}", json=payload)
                response.raise_for_status()
                envelope = response.json()
        except httpx.HTTPStatusError as exc:
            body = exc.response.text[:500]
            raise MeshServiceError(
                f"Mesh service {endpoint} returned HTTP {exc.response.status_code}: {body}"
            ) from exc
        except httpx.HTTPError as exc:
            raise MeshServiceError(
                f"Cannot reach Mesh service at {self.base_url}: {exc}"
            ) from exc

        if envelope.get("status") != "success":
            raise MeshServiceError(
                envelope.get("message") or f"Mesh service {endpoint} failed"
            )
        data = envelope.get("data")
        if not isinstance(data, dict):
            raise MeshServiceError(f"Mesh service {endpoint} returned invalid data")
        return data

    async def health(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/health")
                response.raise_for_status()
                envelope = response.json()
        except httpx.HTTPError as exc:
            raise MeshServiceError(f"Cannot reach Mesh service at {self.base_url}: {exc}") from exc
        if envelope.get("status") != "success":
            raise MeshServiceError(envelope.get("message") or "Mesh service health check failed")
        return envelope.get("data", {})

    async def evaluate_repair_optimize(self, mesh_path: str) -> dict[str, Any]:
        """Send a shared-storage mesh reference through Mesh evaluation and healing."""
        current_path = mesh_path
        initial_analysis = await self._post("/analyze", {"mesh_path": mesh_path})
        evaluation = await self._post("/evaluate", {"mesh_path": current_path})
        defect_report = evaluation.get("defect_report", {})
        found_defects = defect_report.get("summary", {}).get("found", [])

        repair_result: dict[str, Any] = {}
        if found_defects:
            repair_result = await self._post("/repair", {"mesh_path": current_path})
            current_path = repair_result.get("repaired_mesh_path", current_path)

        optimization = await self._post("/optimize", {"mesh_path": current_path})
        optimized_path = optimization.get("optimized_mesh_path", current_path)
        optimized_analysis = await self._post("/analyze", {"mesh_path": optimized_path})
        topology_score = evaluation.get("scores", {}).get("topology")

        return {
            "source_mesh_path": mesh_path,
            "repaired_mesh_path": current_path if repair_result else None,
            "optimized_mesh_path": optimized_path,
            "initial_analysis": initial_analysis,
            "optimized_analysis": optimized_analysis,
            "topology_grade": self._grade(topology_score),
            "quality_scores": evaluation.get("scores", {}),
            "defect_list": found_defects,
            "defect_report": defect_report,
            "repair_actions_taken": repair_result.get("actions", []),
            "optimization_stats": optimization,
        }

    @staticmethod
    def _grade(score: Any) -> str | None:
        if not isinstance(score, (int, float)):
            return None
        if score >= 0.95:
            return "A"
        if score >= 0.85:
            return "B"
        if score >= 0.70:
            return "C"
        if score >= 0.50:
            return "D"
        return "F"

    async def export_mesh(self, mesh_path: str, format: str = "glb") -> dict[str, Any]:
        return await self._post("/export", {"mesh_path": mesh_path, "format": format})


mesh_client = MeshClient()
