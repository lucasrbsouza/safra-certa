from fastapi import APIRouter

from app.api.v1.endpoints import commodities, costs, simulation

router = APIRouter(prefix="/api/v1")

router.include_router(costs.router)
router.include_router(commodities.router)
router.include_router(simulation.router)
