import uuid

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_cost_service
from app.schemas.cost_entry import CostEntryCreate, CostEntryResponse, CostEntryUpdate
from app.services.cost_service import CostService

router = APIRouter(prefix="/costs", tags=["Costs"])

_404 = {404: {"description": "Registro de custo não encontrado."}}
_422 = {422: {"description": "Dados inválidos: cultura não permitida ou valor fora do intervalo `[0, 1.000.000]`."}}


@router.post(
    "",
    response_model=CostEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar custos",
    description="Registra um novo conjunto de custos de produção por hectare para uma cultura (`soja`, `milho` ou `feijao`).",
    response_description="Registro de custo criado com sucesso.",
    responses=_422,
)
def create_cost(data: CostEntryCreate, service: CostService = Depends(get_cost_service)):
    return service.create(data)


@router.get(
    "",
    response_model=list[CostEntryResponse],
    summary="Listar custos",
    description="Retorna todos os registros de custo cadastrados, ordenados por data de criação.",
    response_description="Lista de registros de custo.",
)
def list_costs(service: CostService = Depends(get_cost_service)):
    return service.get_all()


@router.get(
    "/{entry_id}",
    response_model=CostEntryResponse,
    summary="Obter custo por ID",
    description="Retorna um registro de custo específico pelo seu identificador UUID.",
    response_description="Registro de custo encontrado.",
    responses=_404,
)
def get_cost(entry_id: uuid.UUID, service: CostService = Depends(get_cost_service)):
    return service.get_by_id(entry_id)


@router.put(
    "/{entry_id}",
    response_model=CostEntryResponse,
    summary="Atualizar custo",
    description="Atualiza parcialmente um registro de custo existente. Somente os campos informados são alterados.",
    response_description="Registro de custo atualizado.",
    responses={**_404, **_422},
)
def update_cost(
    entry_id: uuid.UUID,
    data: CostEntryUpdate,
    service: CostService = Depends(get_cost_service),
):
    return service.update(entry_id, data)


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir custo",
    description="Remove permanentemente um registro de custo. Operação irreversível.",
    responses=_404,
)
def delete_cost(entry_id: uuid.UUID, service: CostService = Depends(get_cost_service)):
    service.delete(entry_id)
