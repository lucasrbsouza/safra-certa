from fastapi import APIRouter, Depends

from app.core.dependencies import get_simulation_service
from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.services.simulation_service import SimulationService

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.post("", response_model=SimulationResponse)
def run_simulation(
    request: SimulationRequest,
    service: SimulationService = Depends(get_simulation_service),
):
    result = service.simulate(request)
    return SimulationResponse(
        crop_type=result.crop_type,
        total_cost_per_hectare=result.total_cost_per_hectare,
        market_price_per_sack=result.market_price_per_sack,
        breakeven_sacks_per_hectare=result.breakeven_sacks_per_hectare,
        estimated_productivity=result.estimated_productivity,
        profit_loss_per_hectare=result.profit_loss_per_hectare,
        is_viable=result.is_viable,
    )
