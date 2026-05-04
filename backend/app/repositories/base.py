import uuid
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    def __init__(self, db: Session) -> None:
        self._db = db

    @abstractmethod
    def get_by_id(self, entity_id: uuid.UUID) -> T | None: ...

    @abstractmethod
    def get_all(self) -> list[T]: ...

    @abstractmethod
    def create(self, data: Any) -> T: ...

    @abstractmethod
    def delete(self, entity_id: uuid.UUID) -> bool: ...
