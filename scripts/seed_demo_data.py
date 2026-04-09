"""Seed demo data for MEMORA presentations."""

from __future__ import annotations

import asyncio

import httpx

BASE = "http://localhost:8000"

DEMO_CONVERSATIONS = [
    (
        "We're building a B2B SaaS product targeting small and medium businesses. "
        "Our core value prop is affordability - we're going low-cost to penetrate the SMB market fast."
    ),
    (
        "The engineering team is 4 engineers, 1 designer, and 1 PM. "
        "We have a 6-month runway to hit product-market fit."
    ),
    (
        "Tech stack decision: FastAPI for the backend, PostgreSQL for storage, "
        "React for the frontend. We're deploying on AWS using ECS Fargate."
    ),
    (
        "Our pricing model is freemium with a $29/month pro tier. "
        "No enterprise tier for now - we want to stay lean."
    ),
    (
        "Competitor analysis complete. Main competitor charges $199/month. "
        "Our $29 price point is a clear differentiator for budget-conscious SMBs."
    ),
]

CONTRADICTION_MESSAGE = (
    "Executive team meeting today. New direction: we should pivot to enterprise "
    "and charge $299/month. The SMB market is too fragmented."
)


async def main() -> None:
    async with httpx.AsyncClient(timeout=30) as client:
        session_res = await client.post(f"{BASE}/chat/session")
        session_res.raise_for_status()
        session_id = session_res.json()["session_id"]
        print(f"Demo session created: {session_id}")

        for i, message in enumerate(DEMO_CONVERSATIONS, start=1):
            chat_res = await client.post(
                f"{BASE}/chat",
                json={"message": message, "session_id": session_id},
            )
            chat_res.raise_for_status()
            print(f"Seeded conversation {i}/{len(DEMO_CONVERSATIONS)}")
            await asyncio.sleep(3)

        await asyncio.sleep(3)
        contradiction_res = await client.post(
            f"{BASE}/chat",
            json={"message": CONTRADICTION_MESSAGE, "session_id": session_id},
        )
        contradiction_res.raise_for_status()

        print("Injected contradiction message.")
        print(f"SESSION_ID={session_id}")


if __name__ == "__main__":
    asyncio.run(main())
