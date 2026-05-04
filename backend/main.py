from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router
from app.core.config import get_settings
from app.core.database import Base, _get_engine
from app.core.exceptions import (
    CommodityFetchError,
    CostEntryNotFoundError,
    InvalidCostDataError,
    commodity_fetch_handler,
    cost_not_found_handler,
    invalid_cost_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=_get_engine())
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="SafraCerta API",
        version="1.0.0",
        description="Simulador de viabilidade financeira para produtores rurais.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(CostEntryNotFoundError, cost_not_found_handler)
    app.add_exception_handler(CommodityFetchError, commodity_fetch_handler)
    app.add_exception_handler(InvalidCostDataError, invalid_cost_handler)

    app.include_router(router)

    return app


app = create_app()
