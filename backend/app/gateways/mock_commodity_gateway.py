import random

from app.core.exceptions import InvalidCostDataError
from app.domain.value_objects import CropType
from app.gateways.commodity_gateway import CommodityGateway

_BASE_PRICES: dict[str, float] = {
    CropType.SOJA: 127.50,
    CropType.MILHO: 62.80,
    CropType.FEIJAO: 295.00,
}


class MockCommodityGateway(CommodityGateway):
    """Preços realistas fixos com variação de ±2% para simular mercado."""

    def __init__(self, randomize: bool = True) -> None:
        self._randomize = randomize

    async def fetch_price(self, crop_type: str) -> float:
        if crop_type not in _BASE_PRICES:
            raise InvalidCostDataError(f"Cultura '{crop_type}' não suportada pelo gateway mock.")
        base = _BASE_PRICES[crop_type]
        if self._randomize:
            variation = random.uniform(-0.02, 0.02)
            return round(base * (1 + variation), 2)
        return base
