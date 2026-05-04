import uuid

from pydantic import BaseModel, Field, field_validator

from app.domain.value_objects import CropType


class SimulationRequest(BaseModel):
    crop_type: str
    estimated_productivity: float = Field(
        gt=0, le=500, description="Produtividade estimada em sacas/ha"
    )
    cost_entry_id: uuid.UUID | None = None

    @field_validator("crop_type")
    @classmethod
    def validate_crop_type(cls, v: str) -> str:
        return CropType.validate(v)


class SimulationResponse(BaseModel):
    crop_type: str
    total_cost_per_hectare: float
    market_price_per_sack: float
    breakeven_sacks_per_hectare: float
    estimated_productivity: float
    profit_loss_per_hectare: float
    is_viable: bool
    currency: str = "BRL"
