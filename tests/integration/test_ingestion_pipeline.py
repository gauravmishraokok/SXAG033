import pytest
import asyncio
from unittest.mock import AsyncMock
from memora.core.events import EventBus, ConversationTurnEvent, MemoryWriteRequested
from memora.core.types import MemoryType
from memora.core.config import Settings
from memora.core.errors import LLMResponseError
from memora.scheduler.boundary_detector import BoundaryDetector
from memora.scheduler.episode_segmenter import EpisodeSegmenter
from memora.scheduler.type_classifier import TypeClassifier
from memora.scheduler.predict_calibrate import PredictCalibrateLoop
from memora.scheduler.ingestion_pipeline import MemCubeFactory, IngestionPipeline

@pytest.fixture
def bus_and_events():
    bus = EventBus()
    events = []
    
    def on_write(event: MemoryWriteRequested):
        events.append(event)
        
    bus.subscribe(MemoryWriteRequested, on_write)
    return bus, events

def create_pipeline(mock_embedder, mock_llm, bus, flush_on_second=False):
    settings = Settings(episode_buffer_size=5, boundary_threshold=0.8)
    detector = BoundaryDetector(mock_embedder, settings)
    if flush_on_second:
        detector.score = AsyncMock(return_value=0.9) 
    else:
        detector.score = AsyncMock(return_value=0.1)
        
    segmenter = EpisodeSegmenter(detector)
    classifier = TypeClassifier(mock_llm)
    
    retriever = AsyncMock()
    retriever.search.return_value = []
    
    predict_calibrate = PredictCalibrateLoop(retriever, mock_llm)
    
    pipeline = IngestionPipeline(
        segmenter=segmenter,
        classifier=classifier,
        predict_calibrate=predict_calibrate,
        cube_factory=MemCubeFactory(),
        retriever=retriever,
        bus=bus
    )
    return pipeline, segmenter, retriever

@pytest.mark.asyncio
async def test_single_turn_no_episode(mock_embedder, mock_llm, bus_and_events):
    bus, captured_events = bus_and_events
    pipeline, _, _ = create_pipeline(mock_embedder, mock_llm, bus)
    
    await bus.publish(ConversationTurnEvent(user_message="hi", agent_response="hello", session_id="1"))
    
    assert len(captured_events) == 0

@pytest.mark.asyncio
async def test_boundary_triggers_write(mock_embedder, mock_llm, bus_and_events):
    bus, captured_events = bus_and_events
    pipeline, _, _ = create_pipeline(mock_embedder, mock_llm, bus, flush_on_second=True)
    
    await bus.publish(ConversationTurnEvent(user_message="t1", agent_response="r1", session_id="1"))
    await bus.publish(ConversationTurnEvent(user_message="t2", agent_response="r2", session_id="1"))
    
    # Must sleep to allow async event to percolate if event bus was purely async, but it awaits dispatch
    assert len(captured_events) >= 1
    assert captured_events[0].cube.memory_type in [MemoryType.EPISODIC, MemoryType.SEMANTIC]

@pytest.mark.asyncio
async def test_buffer_overflow_triggers_write(mock_embedder, mock_llm, bus_and_events):
    bus, captured_events = bus_and_events
    pipeline, segmenter, _ = create_pipeline(mock_embedder, mock_llm, bus)
    segmenter.detector.buffer_size = 2 
    
    await bus.publish(ConversationTurnEvent(user_message="t1", agent_response="r1", session_id="1"))
    await bus.publish(ConversationTurnEvent(user_message="t2", agent_response="r2", session_id="1"))
    await bus.publish(ConversationTurnEvent(user_message="t3", agent_response="r3", session_id="1"))
    
    assert len(captured_events) >= 1

@pytest.mark.asyncio
async def test_predict_calibrate_deduplication(mock_embedder, mock_llm, bus_and_events, sample_cubes):
    bus, captured_events = bus_and_events
    pipeline, _, retriever = create_pipeline(mock_embedder, mock_llm, bus, flush_on_second=True)
    
    retriever.search.return_value = sample_cubes
    
    mock_llm.complete.return_value = "NO_NEW_INFORMATION"
    mock_llm.complete_json.return_value = {
        "memories": [{"type": "semantic", "content": "test"}]
    }
    
    await bus.publish(ConversationTurnEvent(user_message="t1", agent_response="r1", session_id="1"))
    await bus.publish(ConversationTurnEvent(user_message="t2", agent_response="r2", session_id="1"))
    
    auth_events = [e for e in captured_events if e.cube.memory_type == MemoryType.SEMANTIC]
    assert len(auth_events) == 0

@pytest.mark.asyncio
async def test_classifier_fallback_on_llm_error(mock_embedder, mock_llm, bus_and_events):
    bus, captured_events = bus_and_events
    pipeline, _, _ = create_pipeline(mock_embedder, mock_llm, bus, flush_on_second=True)
    
    mock_llm.complete_json.side_effect = LLMResponseError("failed")
    
    await bus.publish(ConversationTurnEvent(user_message="t1", agent_response="r1", session_id="1"))
    await bus.publish(ConversationTurnEvent(user_message="t2", agent_response="r2", session_id="1"))
    
    assert len(captured_events) == 1
    assert captured_events[0].cube.memory_type == MemoryType.EPISODIC
