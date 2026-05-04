import uuid

from app.core.exceptions import CostEntryNotFoundError
from app.repositories.cost_entry_repository import CostEntryRepository
from app.schemas.cost_entry import CostEntryCreate, CostEntryResponse, CostEntryUpdate


class CostService:
    def __init__(self, repository: CostEntryRepository) -> None:
        self._repo = repository

    def create(self, data: CostEntryCreate) -> CostEntryResponse:
        entry = self._repo.create(data)
        return self._to_response(entry)

    def get_all(self) -> list[CostEntryResponse]:
        return [self._to_response(e) for e in self._repo.get_all()]

    def get_by_id(self, entry_id: uuid.UUID) -> CostEntryResponse:
        entry = self._repo.get_by_id(entry_id)
        if entry is None:
            raise CostEntryNotFoundError(str(entry_id))
        return self._to_response(entry)

    def update(self, entry_id: uuid.UUID, data: CostEntryUpdate) -> CostEntryResponse:
        entry = self._repo.update(entry_id, data)
        if entry is None:
            raise CostEntryNotFoundError(str(entry_id))
        return self._to_response(entry)

    def delete(self, entry_id: uuid.UUID) -> None:
        deleted = self._repo.delete(entry_id)
        if not deleted:
            raise CostEntryNotFoundError(str(entry_id))

    def _to_response(self, entry) -> CostEntryResponse:
        total = (
            float(entry.seeds)
            + float(entry.fertilizers)
            + float(entry.defensivos)
            + float(entry.labor)
            + float(entry.fuel)
            + float(entry.maintenance)
        )
        return CostEntryResponse(
            id=entry.id,
            crop_type=entry.crop_type,
            seeds=float(entry.seeds),
            fertilizers=float(entry.fertilizers),
            defensivos=float(entry.defensivos),
            labor=float(entry.labor),
            fuel=float(entry.fuel),
            maintenance=float(entry.maintenance),
            total_cost=round(total, 2),
            created_at=entry.created_at,
        )
