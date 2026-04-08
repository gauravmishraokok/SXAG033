"""
scheduler/ingestion_pipeline.py — Orchestrates raw conv → episodes → vault write.

This is the entry point for all new memory creation.
It subscribes to ConversationTurnEvent and drives the full write path.

Flow:
    ConversationTurnEvent
        → episode_segmenter.segment(turn_text)        [Nemori]
        → type_classifier.classify(episode)           [MemOS type routing]
        → predict_calibrate.find_gap(episode)         [Nemori predict-calibrate]
        → mem_cube_factory.create(content, type, ...)
        → bus.publish(MemoryWriteRequested(cube))     [→ Court takes over]

Does NOT: write to DB directly (publishes event, Court → Vault handles writes)
Does NOT: know about Court or Vault (only the event bus)
"""
from memora.core.events import bus, ConversationTurnEvent, MemoryWriteRequested
from memora.core.types import MemCube
from .episode_segmenter import EpisodeSegmenter
from .type_classifier import TypeClassifier
from .predict_calibrate import PredictCalibrateLoop
from memora.vault.mem_cube import MemCubeFactory


class IngestionPipeline:
    def __init__(
        self,
        segmenter: EpisodeSegmenter,
        classifier: TypeClassifier,
        predict_calibrate: PredictCalibrateLoop,
        cube_factory: MemCubeFactory,
    ):
        self.segmenter = segmenter
        self.classifier = classifier
        self.predict_calibrate = predict_calibrate
        self.cube_factory = cube_factory
        bus.subscribe(ConversationTurnEvent, self._on_turn)

    async def _on_turn(self, event: ConversationTurnEvent) -> None:
        """Handle a new conversation turn: segment → classify → predict-calibrate → publish."""
        ...
