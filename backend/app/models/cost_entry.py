import uuid
from datetime import datetime

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CostEntry(Base):
    __tablename__ = "cost_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    seeds: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0.0)
    fertilizers: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0.0)
    defensivos: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0.0)
    labor: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0.0)
    fuel: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0.0)
    maintenance: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
