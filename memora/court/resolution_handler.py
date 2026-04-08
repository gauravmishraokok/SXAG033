from memora.core.events import EventBus, ResolutionApplied
from memora.core.interfaces import IQuarantineRepo
from memora.core.types import QuarantineStatus
from memora.core.errors import QuarantineNotFoundError, AlreadyResolvedError

class ResolutionHandler:
    def __init__(self, repo: IQuarantineRepo, bus: EventBus):
        self.repo = repo
        self.bus = bus

    async def resolve(self, quarantine_id: str, resolution: QuarantineStatus, merged_content: str = "") -> None:
        if resolution not in (QuarantineStatus.RESOLVED_ACCEPT, QuarantineStatus.RESOLVED_REJECT, QuarantineStatus.RESOLVED_MERGE):
            raise ValueError(f"Invalid resolution: {resolution}")
            
        if resolution == QuarantineStatus.RESOLVED_MERGE and not merged_content:
            raise ValueError("merged_content is required for RESOLVED_MERGE")

        quarantine_record = await self.repo.get(quarantine_id)
        if not quarantine_record:
            raise QuarantineNotFoundError(f"Quarantine record {quarantine_id} not found")

        if quarantine_record.status != QuarantineStatus.PENDING:
            raise AlreadyResolvedError(f"Quarantine record {quarantine_id} is already resolved")

        await self.repo.resolve(quarantine_id, resolution, merged_content)

        await self.bus.publish(ResolutionApplied(
            quarantine_id=quarantine_id,
            resolution=resolution,
            merged_content=merged_content,
            original_cube_id=quarantine_record.incoming_cube.id,
            session_id=quarantine_record.incoming_cube.provenance.session_id if quarantine_record.incoming_cube.provenance else "unknown"
        ))
