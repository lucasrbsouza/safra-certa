from fastapi import APIRouter, Depends

from app.core.dependencies import get_simulation_service
from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.services.simulation_service import SimulationService

router = APIRouter(prefix="/simulation", tags=["Simulation"])


@router.post(
    "",
    response_model=SimulationResponse,
    summary="Executar simulação de ponto de equilíbrio",
    description=(
        "Calcula o **ponto de equilíbrio** (break-even) em sacas/ha para a cultura informada, "
        "cruzando os custos de produção cadastrados com o preço de mercado atual.\n\n"
        "**Fórmula:** `ponto_equilíbrio = custo_total_por_hectare ÷ preço_por_saca`\n\n"
        "Se `cost_entry_id` for omitido, utiliza os custos mais recentes da cultura selecionada."
    ),
    response_description="Resultado da simulação com ponto de equilíbrio e viabilidade financeira.",
    responses={
        404: {"description": "Registro de custo não encontrado para o ID informado."},
        422: {"description": "Dados de entrada inválidos (cultura incorreta ou produtividade fora do intervalo)."},
        502: {"description": "Falha ao obter cotação de mercado para a cultura solicitada."},
    },
)
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
