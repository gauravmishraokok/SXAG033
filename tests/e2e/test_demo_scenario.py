"""End-to-end demo flow tests for MEMORA API stubs."""

from __future__ import annotations

from fastapi.testclient import TestClient

from memora.api.app import create_app


def test_demo_scenario_flow() -> None:
    """Verify 5-step flow: chat, court queue, resolve, graph, health."""
    client = TestClient(create_app())

    chat_resp = client.post("/chat", json={"message": "We should switch to premium pricing"})
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    assert chat_data["session_id"]
    assert chat_data["memory_count"] >= 0

    queue_resp = client.get("/court/queue")
    assert queue_resp.status_code == 200
    queue = queue_resp.json()
    assert len(queue) >= 1
    quarantine_id = queue[0]["quarantine_id"]

    resolve_resp = client.post(f"/court/resolve/{quarantine_id}", json={"resolution": "accept"})
    assert resolve_resp.status_code == 200
    assert resolve_resp.json()["resolved"] is True

    queue_after_resp = client.get("/court/queue")
    assert queue_after_resp.status_code == 200
    assert len(queue_after_resp.json()) == 0

    graph_nodes_resp = client.get("/graph/nodes")
    assert graph_nodes_resp.status_code == 200
    assert "nodes" in graph_nodes_resp.json()

    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "ok"
