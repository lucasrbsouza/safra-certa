from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.gateways.commodity_gateway import CommodityGateway
from app.gateways.hgbrasil_gateway import HGBrasilGateway
from app.gateways.mock_commodity_gateway import MockCommodityGateway
from app.repositories.commodity_cache_repository import CommodityCacheRepository
from app.repositories.cost_entry_repository import CostEntryRepository
from app.services.commodity_service import CommodityService
from app.services.cost_service import CostService
from app.services.simulation_service import SimulationService


def get_cost_repository(db: Session = Depends(get_db)) -> CostEntryRepository:
    return CostEntryRepository(db)


def get_commodity_cache_repository(db: Session = Depends(get_db)) -> CommodityCacheRepository:
    return CommodityCacheRepository(db)


def get_commodity_gateway(settings: Settings = Depends(get_settings)) -> CommodityGateway:
    if settings.commodity_provider == "hgbrasil":
        return HGBrasilGateway(api_key=settings.hg_brasil_api_key)
    return MockCommodityGateway()


def get_cost_service(repo: CostEntryRepository = Depends(get_cost_repository)) -> CostService:
    return CostService(repo)


def get_commodity_service(
    gateway: CommodityGateway = Depends(get_commodity_gateway),
    cache_repo: CommodityCacheRepository = Depends(get_commodity_cache_repository),
) -> CommodityService:
    return CommodityService(gateway, cache_repo)


def get_simulation_service(
    cost_service: CostService = Depends(get_cost_service),
    commodity_service: CommodityService = Depends(get_commodity_service),
) -> SimulationService:
    return SimulationService(cost_service, commodity_service)
