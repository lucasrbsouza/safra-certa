from datetime import datetime

from pydantic import BaseModel


class CommodityPriceResponse(BaseModel):
    crop_type: str
    price_per_sack: float
    currency: str = "BRL"
    source: str
    fetched_at: datetime
