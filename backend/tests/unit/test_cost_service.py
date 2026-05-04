import uuid

import pytest

from app.core.exceptions import CostEntryNotFoundError
from app.repositories.cost_entry_repository import CostEntryRepository
from app.schemas.cost_entry import CostEntryCreate, CostEntryUpdate
from app.services.cost_service import CostService


@pytest.fixture
def service(db_session):
    return CostService(CostEntryRepository(db_session))


def test_create_returns_correct_total(service):
    data = CostEntryCreate(
        crop_type="soja",
        seeds=1000.0,
        fertilizers=2000.0,
        defensivos=500.0,
        labor=1500.0,
        fuel=400.0,
        maintenance=600.0,
    )
    result = service.create(data)

    assert result.crop_type == "soja"
    assert result.total_cost == 6000.0
    assert result.id is not None


def test_get_all_returns_created_entries(service):
    service.create(CostEntryCreate(crop_type="milho", seeds=500.0))
    service.create(CostEntryCreate(crop_type="feijao", seeds=800.0))

    entries = service.get_all()
    assert len(entries) >= 2


def test_get_by_id_returns_correct_entry(service):
    created = service.create(CostEntryCreate(crop_type="soja", seeds=1200.0))
    fetched = service.get_by_id(created.id)

    assert fetched.id == created.id
    assert fetched.seeds == 1200.0


def test_get_by_id_raises_when_not_found(service):
    with pytest.raises(CostEntryNotFoundError):
        service.get_by_id(uuid.uuid4())


def test_update_partial_fields(service):
    created = service.create(CostEntryCreate(crop_type="soja", seeds=1000.0, labor=2000.0))
    updated = service.update(created.id, CostEntryUpdate(seeds=1500.0))

    assert updated.seeds == 1500.0
    assert updated.labor == 2000.0


def test_update_raises_when_not_found(service):
    with pytest.raises(CostEntryNotFoundError):
        service.update(uuid.uuid4(), CostEntryUpdate(seeds=100.0))


def test_delete_removes_entry(service):
    created = service.create(CostEntryCreate(crop_type="feijao", maintenance=300.0))
    service.delete(created.id)

    with pytest.raises(CostEntryNotFoundError):
        service.get_by_id(created.id)


def test_delete_raises_when_not_found(service):
    with pytest.raises(CostEntryNotFoundError):
        service.delete(uuid.uuid4())
