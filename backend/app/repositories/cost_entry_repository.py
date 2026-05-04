import uuid

from sqlalchemy.orm import Session

from app.models.cost_entry import CostEntry
from app.repositories.base import BaseRepository
from app.schemas.cost_entry import CostEntryCreate, CostEntryUpdate


class CostEntryRepository(BaseRepository[CostEntry]):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_by_id(self, entity_id: uuid.UUID) -> CostEntry | None:
        return self._db.get(CostEntry, entity_id)

    def get_all(self) -> list[CostEntry]:
        return self._db.query(CostEntry).order_by(CostEntry.created_at.desc()).all()

    def get_by_crop_type(self, crop_type: str) -> list[CostEntry]:
        return self._db.query(CostEntry).filter(CostEntry.crop_type == crop_type).all()

    def create(self, data: CostEntryCreate) -> CostEntry:
        entry = CostEntry(**data.model_dump())
        self._db.add(entry)
        self._db.commit()
        self._db.refresh(entry)
        return entry

    def update(self, entity_id: uuid.UUID, data: CostEntryUpdate) -> CostEntry | None:
        entry = self.get_by_id(entity_id)
        if entry is None:
            return None
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(entry, field, value)
        self._db.commit()
        self._db.refresh(entry)
        return entry

    def delete(self, entity_id: uuid.UUID) -> bool:
        entry = self.get_by_id(entity_id)
        if entry is None:
            return False
        self._db.delete(entry)
        self._db.commit()
        return True
