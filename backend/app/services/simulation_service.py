from app.core.exceptions import CommodityFetchError
from app.domain.entities import CostBreakdown, SimulationResult
from app.schemas.simulation import SimulationRequest
from app.services.commodity_service import CommodityService
from app.services.cost_service import CostService


class SimulationService:
    def __init__(self, cost_service: CostService, commodity_service: CommodityService) -> None:
        self._costs = cost_service
        self._commodities = commodity_service

    def simulate(self, request: SimulationRequest) -> SimulationResult:
        breakdown = self._resolve_costs(request)
        commodity = self._commodities.get_price(request.crop_type)

        if commodity.price_per_sack <= 0:
            raise CommodityFetchError("Preço de mercado inválido: deve ser maior que zero.")

        total_cost = breakdown.total()

        # RN01: unidade = sacas de 60kg/ha
        # RF03: Ponto de Equilíbrio = Custo Total / Preço por Saca
        breakeven = total_cost / commodity.price_per_sack

        profit_loss = (request.estimated_productivity - breakeven) * commodity.price_per_sack
        is_viable = request.estimated_productivity >= breakeven

        return SimulationResult(
            crop_type=request.crop_type,
            total_cost_per_hectare=round(total_cost, 2),
            market_price_per_sack=commodity.price_per_sack,
            breakeven_sacks_per_hectare=round(breakeven, 2),
            estimated_productivity=request.estimated_productivity,
            profit_loss_per_hectare=round(profit_loss, 2),
            is_viable=is_viable,
        )

    def _resolve_costs(self, request: SimulationRequest) -> CostBreakdown:
        if request.cost_entry_id is not None:
            entry = self._costs.get_by_id(request.cost_entry_id)
            return CostBreakdown(
                seeds=entry.seeds,
                fertilizers=entry.fertilizers,
                defensivos=entry.defensivos,
                labor=entry.labor,
                fuel=entry.fuel,
                maintenance=entry.maintenance,
            )
        # Simulação sem entrada salva: todos os custos zerados (demo rápido)
        return CostBreakdown(
            seeds=0.0,
            fertilizers=0.0,
            defensivos=0.0,
            labor=0.0,
            fuel=0.0,
            maintenance=0.0,
        )
