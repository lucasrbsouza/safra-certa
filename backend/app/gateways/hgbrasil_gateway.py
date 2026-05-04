import httpx

from app.core.exceptions import CommodityFetchError, InvalidCostDataError
from app.domain.value_objects import CropType
from app.gateways.commodity_gateway import CommodityGateway

# Mapeamento HG Brasil → CropType
_HG_SYMBOL_MAP: dict[str, str] = {
    CropType.SOJA: "SOYBEAN",
    CropType.MILHO: "CORN",
}

# feijão não é disponibilizado pela HG Brasil — fallback fixo
_FEIJAO_FALLBACK_BRL = 295.00

# Conversão: bushel → saca de 60kg (1 bushel soja ≈ 27.216 kg)
_KG_PER_BUSHEL_SOJA = 27.216
_KG_PER_BUSHEL_MILHO = 25.401
_SACK_KG = 60.0

_KG_PER_BUSHEL: dict[str, float] = {
    CropType.SOJA: _KG_PER_BUSHEL_SOJA,
    CropType.MILHO: _KG_PER_BUSHEL_MILHO,
}


class HGBrasilGateway(CommodityGateway):
    _BASE_URL = "https://api.hgbrasil.com/finance"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def fetch_price(self, crop_type: str) -> float:
        if crop_type == CropType.FEIJAO:
            return _FEIJAO_FALLBACK_BRL

        symbol = _HG_SYMBOL_MAP.get(crop_type)
        if symbol is None:
            raise InvalidCostDataError(f"Cultura '{crop_type}' não mapeada para HG Brasil.")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self._BASE_URL,
                    params={"key": self._api_key, "format": "json-cors"},
                )
                response.raise_for_status()
                data = response.json()

            usd_brl = float(data["results"]["currencies"]["USD"]["buy"])
            usd_per_bushel = float(data["results"]["stocks"][symbol]["price"])
            kg_per_bushel = _KG_PER_BUSHEL[crop_type]
            price_brl_per_sack = (usd_per_bushel / kg_per_bushel) * _SACK_KG * usd_brl
            return round(price_brl_per_sack, 2)

        except (httpx.HTTPError, KeyError, ValueError) as exc:
            raise CommodityFetchError(f"Falha ao buscar cotação HG Brasil para '{crop_type}': {exc}") from exc
