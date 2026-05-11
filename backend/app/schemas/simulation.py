import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.value_objects import CropType


class SimulationRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "crop_type": "soja",
                "estimated_productivity": 60.0,
                "cost_entry_id": None,
            }
        }
    )

    crop_type: str = Field(description="Tipo de cultura a simular. Valores aceitos: `soja`, `milho`, `feijao`.")
    estimated_productivity: float = Field(
        gt=0,
        le=500,
        description="Produtividade estimada da lavoura em sacas/ha. Intervalo: `(0, 500]`.",
    )
    cost_entry_id: uuid.UUID | None = Field(
        default=None,
        description=(
            "ID de um registro de custo específico a usar na simulação. "
            "Se `null`, utiliza o registro mais recente da cultura informada."
        ),
    )

    @field_validator("crop_type")
    @classmethod
    def validate_crop_type(cls, v: str) -> str:
        return CropType.validate(v)


class SimulationResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "crop_type": "soja",
                "total_cost_per_hectare": 3250.00,
                "market_price_per_sack": 127.50,
                "breakeven_sacks_per_hectare": 25.49,
                "estimated_productivity": 60.0,
                "profit_loss_per_hectare": 4400.00,
                "is_viable": True,
                "currency": "BRL",
            }
        }
    )

    crop_type: str = Field(description="Tipo de cultura simulada.")
    total_cost_per_hectare: float = Field(description="Custo total de produção em R$/ha.")
    market_price_per_sack: float = Field(description="Preço de mercado atual em R$/saca de 60 kg.")
    breakeven_sacks_per_hectare: float = Field(
        description="Ponto de equilíbrio calculado: quantidade mínima de sacas/ha para cobrir os custos."
    )
    estimated_productivity: float = Field(description="Produtividade estimada informada na requisição (sc/ha).")
    profit_loss_per_hectare: float = Field(
        description="Margem estimada em R$/ha. Positivo = lucro, negativo = prejuízo."
    )
    is_viable: bool = Field(
        description="`true` quando `estimated_productivity ≥ breakeven_sacks_per_hectare`."
    )
    currency: str = Field(default="BRL", description="Moeda de referência. Sempre `BRL`.")
