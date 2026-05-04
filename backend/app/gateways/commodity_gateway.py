from abc import ABC, abstractmethod


class CommodityGateway(ABC):
    """Strategy interface for commodity price providers."""

    @abstractmethod
    async def fetch_price(self, crop_type: str) -> float:
        """Retorna o preço em BRL por saca de 60kg."""
        ...
