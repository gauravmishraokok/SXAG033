"""Chat router endpoints."""

from __future__ import annotations

import time

from fastapi import APIRouter, Depends, HTTPException

from memora.agent.memora_agent import MemoraAgent
from memora.api.demo_court import check_and_inject
from memora.api.dependencies import get_agent, get_cube_factory, get_episodic_repo, get_kg_repo, get_semantic_repo
from memora.api.routers.health import _latency_samples
from memora.api.schemas.chat_schemas import ChatRequest, ChatResponse
from memora.api.turn_distillation import distill_chat_turn, semantic_key
from memora.core.types import MemoryType
from memora.vault.episodic_repo import EpisodicRepo
from memora.vault.kg_repo import KGRepo
from memora.vault.mem_cube import MemCubeFactory
from memora.vault.semantic_repo import SemanticRepo

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def post_chat(
    payload: ChatRequest,
    agent: MemoraAgent = Depends(get_agent),
    cube_factory: MemCubeFactory = Depends(get_cube_factory),
    episodic_repo: EpisodicRepo = Depends(get_episodic_repo),
    semantic_repo: SemanticRepo = Depends(get_semantic_repo),
    kg_repo: KGRepo = Depends(get_kg_repo),
) -> ChatResponse:
    """Process one chat turn against the real agent."""
    t0 = time.time()

    # Hardcoded contradiction detection — fires before the agent responds
    # so the court card is visible almost immediately after the user sends.
    check_and_inject(payload.message)

    session_id = payload.session_id or agent.session_manager.create_session()
    if payload.session_id:
        agent.session_manager.ensure_session(session_id)
    try:
        response = await agent.chat(
            message=payload.message,
            session_id=session_id,
            feedback=payload.feedback,
        )
    except Exception:
        turn_number = agent.session_manager.increment_turn(session_id)
        response = ChatResponse(
            text="I am online, but the LLM provider is currently unavailable. Please verify GROQ_API_KEY and retry.",
            session_id=session_id,
            turn_number=turn_number,
            memories_used=[],
            memory_count=0,
        )
        _latency_samples.append((time.time() - t0) * 1000.0)
        if len(_latency_samples) > 1000:
            _latency_samples.pop(0)
        return response

    # Distill turn into episodic + semantic + KG memories (compact, not raw transcript).
    try:
        distilled = await distill_chat_turn(agent.llm, payload.message, response.text)
        sid = response.session_id

        if distilled.get("episodic_line"):
            cube = await cube_factory.create(
                content=distilled["episodic_line"],
                memory_type=MemoryType.EPISODIC,
                session_id=sid,
                origin="chat_turn",
                tags=["chat", "episodic"],
                extra={"label": distilled["episodic_line"][:120]},
            )
            await episodic_repo.save(cube)

        for fact in distilled.get("semantic_facts") or []:
            if len(fact) < 3:
                continue
            key = semantic_key(sid, fact)
            sem = await cube_factory.create(
                content=fact,
                memory_type=MemoryType.SEMANTIC,
                session_id=sid,
                origin="chat_distill",
                tags=["chat", "semantic"],
                extra={"key": key},
            )
            await semantic_repo.upsert_by_key(key, sem)

        prev_kg: str | None = None
        for ent in distilled.get("kg_entities") or []:
            title = (ent.get("title") or "").strip()
            detail = (ent.get("detail") or "").strip()
            if not title:
                continue
            body = f"{title}\n{detail}" if detail else title
            kg_cube = await cube_factory.create(
                content=body,
                memory_type=MemoryType.KG_NODE,
                session_id=sid,
                origin="chat_distill",
                tags=["chat", "kg"],
                extra={"label": title, "detail": detail},
            )
            try:
                await kg_repo.upsert_node(kg_cube)
                if prev_kg:
                    try:
                        await kg_repo.add_edge(prev_kg, kg_cube.id, "related", {"session_id": sid})
                    except Exception:
                        pass
                prev_kg = kg_cube.id
            except Exception:
                pass
    except Exception:
        pass

    _latency_samples.append((time.time() - t0) * 1000.0)
    if len(_latency_samples) > 1000:
        _latency_samples.pop(0)

    return ChatResponse(
        text=response.text,
        session_id=response.session_id,
        turn_number=response.turn_number,
        memories_used=response.memories_used,
        memory_count=response.memory_count,
    )


@router.post("/session")
async def create_session(agent: MemoraAgent = Depends(get_agent)) -> dict[str, str]:
    """Create and return a new session identifier."""
    session_id = agent.session_manager.create_session()
    return {"session_id": session_id}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str, agent: MemoraAgent = Depends(get_agent)) -> dict:
    """Return stored session state."""
    try:
        state = agent.session_manager.get(session_id)
        return {
            "session_id": state.session_id,
            "turn_count": state.turn_count,
            "created_at": state.created_at.isoformat(),
            "last_active_at": state.last_active_at.isoformat(),
        }
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Session not found") from exc
