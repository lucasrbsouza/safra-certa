from fastapi import APIRouter, Depends

from app.core.dependencies import get_commodity_service
from app.domain.value_objects import CropType
from app.schemas.commodity import CommodityPriceResponse
from app.services.commodity_service import CommodityService

router = APIRouter(prefix="/commodities", tags=["Market"])


@router.get("", response_model=list[CommodityPriceResponse])
def list_prices(service: CommodityService = Depends(get_commodity_service)):
    return service.get_all_prices()


@router.get("/{crop_type}", response_model=CommodityPriceResponse)
def get_price(crop_type: str, service: CommodityService = Depends(get_commodity_service)):
    CropType.validate(crop_type)
    return service.get_price(crop_type)


@router.post("/refresh", response_model=list[CommodityPriceResponse])
def refresh_prices(service: CommodityService = Depends(get_commodity_service)):
    return service.refresh_all()
