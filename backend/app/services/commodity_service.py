import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.domain.value_objects import CropType
from app.gateways.commodity_gateway import CommodityGateway
from app.repositories.commodity_cache_repository import CommodityCacheRepository
from app.schemas.commodity import CommodityPriceResponse

_executor = ThreadPoolExecutor(max_workers=4)


def _run_async(coro):
    """Run an async coroutine from a sync context safely."""
    try:
        asyncio.get_running_loop()
        # Inside an async context — delegate to a thread with its own event loop
        future = _executor.submit(asyncio.run, coro)
        return future.result()
    except RuntimeError:
        # No running loop — safe to call asyncio.run directly
        return asyncio.run(coro)


class CommodityService:
    def __init__(self, gateway: CommodityGateway, cache_repo: CommodityCacheRepository) -> None:
        self._gateway = gateway
        self._cache = cache_repo

    def get_price(self, crop_type: str) -> CommodityPriceResponse:
        if not self._cache.is_stale(crop_type):
            cached = self._cache.get_by_crop_type(crop_type)
            return CommodityPriceResponse(
                crop_type=crop_type,
                price_per_sack=float(cached.price_per_sack),
                source=cached.source,
                fetched_at=cached.fetched_at,
            )

        price = _run_async(self._gateway.fetch_price(crop_type))
        source = type(self._gateway).__name__
        cached = self._cache.upsert(crop_type, price, source)
        return CommodityPriceResponse(
            crop_type=crop_type,
            price_per_sack=float(cached.price_per_sack),
            source=cached.source,
            fetched_at=cached.fetched_at,
        )

    def get_all_prices(self) -> list[CommodityPriceResponse]:
        return [self.get_price(crop) for crop in CropType.VALID]

    def refresh_all(self) -> list[CommodityPriceResponse]:
        results = []
        for crop in CropType.VALID:
            price = _run_async(self._gateway.fetch_price(crop))
            source = type(self._gateway).__name__
            cached = self._cache.upsert(crop, price, source)
            results.append(
                CommodityPriceResponse(
                    crop_type=crop,
                    price_per_sack=float(cached.price_per_sack),
                    source=cached.source,
                    fetched_at=cached.fetched_at,
                )
            )
        return results
