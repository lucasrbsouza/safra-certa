from datetime import datetime

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CommodityCache(Base):
    __tablename__ = "commodity_cache"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    crop_type: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    price_per_sack: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
