import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.value_objects import CropType

_CROP_TYPE_DESC = "Tipo de cultura. Valores aceitos: `soja`, `milho`, `feijao`."
_COST_RANGE_DESC = "Custo em R$/ha. Intervalo permitido: `[0, 1.000.000]`."


def _cost_field(default: float = 0.0, description: str = _COST_RANGE_DESC) -> float:
    return Field(default=default, ge=0, le=1_000_000, description=description)


class CostEntryCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "crop_type": "soja",
                "seeds": 350.00,
                "fertilizers": 1200.00,
                "defensivos": 850.00,
                "labor": 420.00,
                "fuel": 280.00,
                "maintenance": 150.00,
            }
        }
    )

    crop_type: str = Field(description=_CROP_TYPE_DESC)
    seeds: float = _cost_field(description="Custo com sementes (R$/ha).")
    fertilizers: float = _cost_field(description="Custo com fertilizantes (R$/ha).")
    defensivos: float = _cost_field(description="Custo com defensivos agrícolas (R$/ha).")
    labor: float = _cost_field(description="Custo com mão de obra (R$/ha).")
    fuel: float = _cost_field(description="Custo com combustível (R$/ha).")
    maintenance: float = _cost_field(description="Custo com manutenção de equipamentos (R$/ha).")

    @field_validator("crop_type")
    @classmethod
    def validate_crop_type(cls, v: str) -> str:
        return CropType.validate(v)


class CostEntryUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fertilizers": 1350.00,
                "fuel": 310.00,
            }
        }
    )

    seeds: float | None = Field(default=None, ge=0, le=1_000_000, description="Custo com sementes (R$/ha).")
    fertilizers: float | None = Field(default=None, ge=0, le=1_000_000, description="Custo com fertilizantes (R$/ha).")
    defensivos: float | None = Field(default=None, ge=0, le=1_000_000, description="Custo com defensivos agrícolas (R$/ha).")
    labor: float | None = Field(default=None, ge=0, le=1_000_000, description="Custo com mão de obra (R$/ha).")
    fuel: float | None = Field(default=None, ge=0, le=1_000_000, description="Custo com combustível (R$/ha).")
    maintenance: float | None = Field(default=None, ge=0, le=1_000_000, description="Custo com manutenção de equipamentos (R$/ha).")


class CostEntryResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "crop_type": "soja",
                "seeds": 350.00,
                "fertilizers": 1200.00,
                "defensivos": 850.00,
                "labor": 420.00,
                "fuel": 280.00,
                "maintenance": 150.00,
                "total_cost": 3250.00,
                "created_at": "2025-01-15T10:30:00",
            }
        },
    )

    id: uuid.UUID = Field(description="Identificador único do registro.")
    crop_type: str = Field(description=_CROP_TYPE_DESC)
    seeds: float = Field(description="Custo com sementes (R$/ha).")
    fertilizers: float = Field(description="Custo com fertilizantes (R$/ha).")
    defensivos: float = Field(description="Custo com defensivos agrícolas (R$/ha).")
    labor: float = Field(description="Custo com mão de obra (R$/ha).")
    fuel: float = Field(description="Custo com combustível (R$/ha).")
    maintenance: float = Field(description="Custo com manutenção de equipamentos (R$/ha).")
    total_cost: float = Field(description="Soma de todos os custos (R$/ha). Campo calculado.")
    created_at: datetime = Field(description="Data e hora de criação do registro (UTC).")
