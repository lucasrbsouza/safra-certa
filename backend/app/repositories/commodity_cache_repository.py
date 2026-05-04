from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.models.commodity_cache import CommodityCache


class CommodityCacheRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_crop_type(self, crop_type: str) -> CommodityCache | None:
        return self._db.query(CommodityCache).filter(CommodityCache.crop_type == crop_type).first()

    def upsert(self, crop_type: str, price: float, source: str) -> CommodityCache:
        cache = self.get_by_crop_type(crop_type)
        if cache:
            cache.price_per_sack = price
            cache.source = source
            cache.fetched_at = datetime.now(UTC)
        else:
            cache = CommodityCache(crop_type=crop_type, price_per_sack=price, source=source)
            self._db.add(cache)
        self._db.commit()
        self._db.refresh(cache)
        return cache

    def is_stale(self, crop_type: str, max_age_hours: int = 24) -> bool:
        cache = self.get_by_crop_type(crop_type)
        if cache is None:
            return True
        age = datetime.now(UTC) - cache.fetched_at.replace(tzinfo=UTC)
        return age > timedelta(hours=max_age_hours)
