import uuid

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_cost_service
from app.schemas.cost_entry import CostEntryCreate, CostEntryResponse, CostEntryUpdate
from app.services.cost_service import CostService

router = APIRouter(prefix="/costs", tags=["Costs"])


@router.post("", response_model=CostEntryResponse, status_code=status.HTTP_201_CREATED)
def create_cost(data: CostEntryCreate, service: CostService = Depends(get_cost_service)):
    return service.create(data)


@router.get("", response_model=list[CostEntryResponse])
def list_costs(service: CostService = Depends(get_cost_service)):
    return service.get_all()


@router.get("/{entry_id}", response_model=CostEntryResponse)
def get_cost(entry_id: uuid.UUID, service: CostService = Depends(get_cost_service)):
    return service.get_by_id(entry_id)


@router.put("/{entry_id}", response_model=CostEntryResponse)
def update_cost(
    entry_id: uuid.UUID,
    data: CostEntryUpdate,
    service: CostService = Depends(get_cost_service),
):
    return service.update(entry_id, data)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost(entry_id: uuid.UUID, service: CostService = Depends(get_cost_service)):
    service.delete(entry_id)
