"""
Run with: poetry run python scripts/api_audit.py
Verifies every API endpoint returns the expected shape.
"""

import asyncio
import sys

import httpx

BASE = "http://localhost:8000"
PASS = "OK"
FAIL = "FAIL"
results = []


async def check(label, method, path, body=None, expect_keys=None):
    async with httpx.AsyncClient() as client:
        if method == "GET":
            r = await client.get(f"{BASE}{path}", timeout=10)
        else:
            r = await client.post(f"{BASE}{path}", json=body, timeout=10)

    if r.status_code >= 400:
        print(f"{FAIL} {label}: HTTP {r.status_code} - {r.text[:200]}")
        results.append(False)
        return

    data = r.json()
    if expect_keys:
        missing = [k for k in expect_keys if k not in data]
        if missing:
            print(f"{FAIL} {label}: missing keys {missing} in {list(data.keys())}")
            results.append(False)
            return

    print(f"{PASS} {label}: {r.status_code}")
    results.append(True)


async def main():
    print("\n=== MEMORA API AUDIT ===\n")

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/chat/session")
        session_id = r.json()["session_id"]
        print(f"Session: {session_id}\n")

    await check(
        "GET /health",
        "GET",
        "/health",
        expect_keys=[
            "status",
            "total_memories",
            "db_connected",
            "memories_by_tier",
            "memories_by_type",
            "quarantine_pending",
        ],
    )
    await check("POST /chat/session", "POST", "/chat/session", expect_keys=["session_id"])
    await check(
        "POST /chat",
        "POST",
        "/chat",
        body={"message": "What is our pricing strategy?", "session_id": session_id},
        expect_keys=["text", "session_id", "turn_number", "memories_used", "memory_count"],
    )
    await asyncio.sleep(3)
    await check(
        "GET /memories?session_id",
        "GET",
        f"/memories?session_id={session_id}&limit=20",
        expect_keys=["memories", "total"],
    )
    await check(
        "GET /memories/search",
        "GET",
        "/memories/search?q=pricing&top_k=5",
        expect_keys=["memories", "total"],
    )
    await check("GET /court/queue", "GET", "/court/queue")
    await check(
        "GET /court/health",
        "GET",
        "/court/health",
        expect_keys=[
            "pending_count",
            "resolved_today",
            "total_quarantined_all_time",
            "average_contradiction_score",
        ],
    )
    await check("GET /graph/nodes", "GET", "/graph/nodes", expect_keys=["nodes"])
    await check("GET /graph/edges", "GET", "/graph/edges", expect_keys=["edges"])
    await check(
        "GET /timeline",
        "GET",
        f"/timeline?session_id={session_id}&limit=50",
        expect_keys=["events", "total"],
    )

    print(f"\n=== RESULTS: {sum(results)}/{len(results)} passed ===\n")
    if not all(results):
        sys.exit(1)


asyncio.run(main())
