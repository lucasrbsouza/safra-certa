from fastapi import Request
from fastapi.responses import JSONResponse


class SafraCertaError(Exception):
    pass


class CostEntryNotFoundError(SafraCertaError):
    def __init__(self, entry_id: str):
        super().__init__(f"Cost entry '{entry_id}' not found.")


class CommodityFetchError(SafraCertaError):
    pass


class InvalidCostDataError(SafraCertaError):
    pass


async def cost_not_found_handler(request: Request, exc: CostEntryNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc), "code": "COST_NOT_FOUND"})


async def commodity_fetch_handler(request: Request, exc: CommodityFetchError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc), "code": "COMMODITY_FETCH_ERROR"})


async def invalid_cost_handler(request: Request, exc: InvalidCostDataError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc), "code": "INVALID_COST_DATA"})
