import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.value_objects import CropType


def _cost_field(default: float = 0.0) -> float:
    # OWASP: rejeita valores negativos e absurdamente altos
    return Field(default=default, ge=0, le=1_000_000)


class CostEntryCreate(BaseModel):
    crop_type: str
    seeds: float = _cost_field()
    fertilizers: float = _cost_field()
    defensivos: float = _cost_field()
    labor: float = _cost_field()
    fuel: float = _cost_field()
    maintenance: float = _cost_field()

    @field_validator("crop_type")
    @classmethod
    def validate_crop_type(cls, v: str) -> str:
        # OWASP: whitelist — rejeita qualquer valor fora do domínio
        return CropType.validate(v)


class CostEntryUpdate(BaseModel):
    seeds: float | None = Field(default=None, ge=0, le=1_000_000)
    fertilizers: float | None = Field(default=None, ge=0, le=1_000_000)
    defensivos: float | None = Field(default=None, ge=0, le=1_000_000)
    labor: float | None = Field(default=None, ge=0, le=1_000_000)
    fuel: float | None = Field(default=None, ge=0, le=1_000_000)
    maintenance: float | None = Field(default=None, ge=0, le=1_000_000)


class CostEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    crop_type: str
    seeds: float
    fertilizers: float
    defensivos: float
    labor: float
    fuel: float
    maintenance: float
    total_cost: float
    created_at: datetime
