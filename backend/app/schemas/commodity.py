from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommodityPriceResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "crop_type": "soja",
                "price_per_sack": 127.50,
                "currency": "BRL",
                "source": "mock",
                "fetched_at": "2025-01-15T10:00:00",
            }
        }
    )

    crop_type: str = Field(description="Tipo de cultura: `soja`, `milho` ou `feijao`.")
    price_per_sack: float = Field(description="Preço de mercado em R$ por saca de 60 kg.")
    currency: str = Field(default="BRL", description="Moeda da cotação. Sempre `BRL`.")
    source: str = Field(description="Origem dos dados: `mock` (fixo) ou `hgbrasil` (tempo real).")
    fetched_at: datetime = Field(description="Data e hora da última atualização da cotação (UTC).")
