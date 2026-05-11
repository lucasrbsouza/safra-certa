from fastapi import APIRouter, Depends

from app.core.dependencies import get_commodity_service
from app.domain.value_objects import CropType
from app.schemas.commodity import CommodityPriceResponse
from app.services.commodity_service import CommodityService

router = APIRouter(prefix="/commodities", tags=["Market"])

_502 = {502: {"description": "Falha ao obter cotações da API de origem (HG Brasil ou similar)."}}
_404 = {404: {"description": "Cultura não encontrada ou cotação indisponível."}}
_422 = {422: {"description": "Tipo de cultura inválido. Valores aceitos: `soja`, `milho`, `feijao`."}}


@router.get(
    "",
    response_model=list[CommodityPriceResponse],
    summary="Listar cotações",
    description=(
        "Retorna as cotações atuais de **soja**, **milho** e **feijão** em R$/saca de 60 kg. "
        "Os dados são servidos a partir de cache com TTL de 24 horas."
    ),
    response_description="Lista de cotações de commodities agrícolas.",
    responses=_502,
)
def list_prices(service: CommodityService = Depends(get_commodity_service)):
    return service.get_all_prices()


@router.get(
    "/{crop_type}",
    response_model=CommodityPriceResponse,
    summary="Obter cotação por cultura",
    description="Retorna a cotação atual de uma cultura específica (`soja`, `milho` ou `feijao`) em R$/saca de 60 kg.",
    response_description="Cotação da cultura solicitada.",
    responses={**_404, **_422, **_502},
)
def get_price(crop_type: str, service: CommodityService = Depends(get_commodity_service)):
    CropType.validate(crop_type)
    return service.get_price(crop_type)


@router.post(
    "/refresh",
    response_model=list[CommodityPriceResponse],
    summary="Forçar atualização de cotações",
    description=(
        "Invalida o cache e busca as cotações mais recentes diretamente na API de origem. "
        "Use com moderação — a API de origem possui limite de requisições diárias."
    ),
    response_description="Lista de cotações atualizadas.",
    responses=_502,
)
def refresh_prices(service: CommodityService = Depends(get_commodity_service)):
    return service.refresh_all()
