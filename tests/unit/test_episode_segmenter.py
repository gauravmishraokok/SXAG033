import pytest
from unittest.mock import AsyncMock
from memora.core.config import Settings
from memora.scheduler.boundary_detector import BoundaryDetector
from memora.scheduler.episode_segmenter import EpisodeSegmenter

@pytest.mark.asyncio
async def test_single_turn_no_episode(mock_embedder):
    settings = Settings(episode_buffer_size=5, boundary_threshold=0.8)
    detector = BoundaryDetector(mock_embedder, settings)
    segmenter = EpisodeSegmenter(detector)
    
    episode = await segmenter.process_turn("hello", "session-1")
    assert episode is None
    
@pytest.mark.asyncio
async def test_boundary_triggers_write(mock_embedder):
    settings = Settings(episode_buffer_size=5, boundary_threshold=0.1)
    detector = BoundaryDetector(mock_embedder, settings)
    segmenter = EpisodeSegmenter(detector)
    
    detector.score = AsyncMock(return_value=0.9)
    
    await segmenter.process_turn("hello", "session-1")
    episode = await segmenter.process_turn("completely different", "session-1")
    
    assert episode is not None
    assert "hello" in episode.content

@pytest.mark.asyncio
async def test_buffer_overflow_triggers_write(mock_embedder):
    settings = Settings(episode_buffer_size=2, boundary_threshold=0.9)
    detector = BoundaryDetector(mock_embedder, settings)
    segmenter = EpisodeSegmenter(detector)
    
    detector.score = AsyncMock(return_value=0.1)
    
    await segmenter.process_turn("t1", "session")
    await segmenter.process_turn("t2", "session")
    episode = await segmenter.process_turn("t3", "session")
    assert episode is not None
