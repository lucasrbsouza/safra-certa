"""
Testes unitários do motor de cálculo de Ponto de Equilíbrio (RF03).

Todos os valores esperados foram verificados manualmente:
  Fórmula: breakeven = custo_total_ha / preco_saca
  Lucro/Prejuízo = (produtividade - breakeven) * preco_saca
"""

import pytest

from app.core.exceptions import CommodityFetchError
from app.domain.entities import CostBreakdown
from app.repositories.commodity_cache_repository import CommodityCacheRepository
from app.repositories.cost_entry_repository import CostEntryRepository
from app.schemas.simulation import SimulationRequest
from app.services.commodity_service import CommodityService
from app.services.cost_service import CostService
from app.services.simulation_service import SimulationService


def _make_service(db_session, mock_gateway):
    cost_repo = CostEntryRepository(db_session)
    cache_repo = CommodityCacheRepository(db_session)
    cost_service = CostService(cost_repo)
    commodity_service = CommodityService(mock_gateway, cache_repo)
    return SimulationService(cost_service, commodity_service)


# --- Testes puros de CostBreakdown.total() ---

def test_cost_breakdown_total_all_fields():
    breakdown = CostBreakdown(
        seeds=1000.0,
        fertilizers=2000.0,
        defensivos=1500.0,
        labor=2500.0,
        fuel=800.0,
        maintenance=700.0,
    )
    assert breakdown.total() == 8500.0


def test_cost_breakdown_total_with_zeros():
    breakdown = CostBreakdown(
        seeds=4000.0,
        fertilizers=0.0,
        defensivos=0.0,
        labor=2000.0,
        fuel=0.0,
        maintenance=0.0,
    )
    assert breakdown.total() == 6000.0


def test_cost_breakdown_total_all_zero():
    breakdown = CostBreakdown(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    assert breakdown.total() == 0.0


# --- Testes do SimulationService ---

def test_breakeven_soja_calculo_correto(db_session, mock_gateway):
    """
    Custo: R$8.500/ha | Preço Soja: R$127,50/saca
    Breakeven esperado: 8500 / 127.50 = 66.67 sacas/ha
    """
    service = _make_service(db_session, mock_gateway)
    request = SimulationRequest(crop_type="soja", estimated_productivity=70.0)
    result = service.simulate(request)

    assert result.crop_type == "soja"
    assert result.market_price_per_sack == 127.50
    assert result.total_cost_per_hectare == 0.0
    assert result.breakeven_sacks_per_hectare == 0.0
    assert result.is_viable is True


def test_breakeven_com_custo_real_soja(db_session, mock_gateway):
    """
    Custo total: R$8.500/ha | Preço: R$127,50/saca
    Breakeven: 66.67 sacas/ha
    """
    from app.repositories.cost_entry_repository import CostEntryRepository
    from app.schemas.cost_entry import CostEntryCreate

    repo = CostEntryRepository(db_session)
    entry = repo.create(CostEntryCreate(
        crop_type="soja",
        seeds=1000.0,
        fertilizers=2000.0,
        defensivos=1500.0,
        labor=2500.0,
        fuel=800.0,
        maintenance=700.0,
    ))

    service = _make_service(db_session, mock_gateway)
    request = SimulationRequest(
        crop_type="soja",
        estimated_productivity=70.0,
        cost_entry_id=entry.id,
    )
    result = service.simulate(request)

    assert result.total_cost_per_hectare == 8500.0
    assert result.breakeven_sacks_per_hectare == round(8500.0 / 127.50, 2)


def test_simulacao_viavel_quando_produtividade_supera_breakeven(db_session, mock_gateway):
    """Produtividade 70 sacas > breakeven 66.67 → viável"""
    from app.repositories.cost_entry_repository import CostEntryRepository
    from app.schemas.cost_entry import CostEntryCreate

    repo = CostEntryRepository(db_session)
    entry = repo.create(CostEntryCreate(
        crop_type="soja", seeds=1000.0, fertilizers=2000.0, defensivos=1500.0,
        labor=2500.0, fuel=800.0, maintenance=700.0,
    ))

    service = _make_service(db_session, mock_gateway)
    result = service.simulate(SimulationRequest(
        crop_type="soja", estimated_productivity=70.0, cost_entry_id=entry.id
    ))

    assert result.is_viable is True
    assert result.profit_loss_per_hectare > 0


def test_simulacao_inviavel_quando_produtividade_abaixo_breakeven(db_session, mock_gateway):
    """Produtividade 50 sacas < breakeven 66.67 → inviável"""
    from app.repositories.cost_entry_repository import CostEntryRepository
    from app.schemas.cost_entry import CostEntryCreate

    repo = CostEntryRepository(db_session)
    entry = repo.create(CostEntryCreate(
        crop_type="soja", seeds=1000.0, fertilizers=2000.0, defensivos=1500.0,
        labor=2500.0, fuel=800.0, maintenance=700.0,
    ))

    service = _make_service(db_session, mock_gateway)
    result = service.simulate(SimulationRequest(
        crop_type="soja", estimated_productivity=50.0, cost_entry_id=entry.id
    ))

    assert result.is_viable is False
    assert result.profit_loss_per_hectare < 0


def test_formula_lucro_prejuizo_correto(db_session, mock_gateway):
    """
    Custo: R$8.500/ha | Preço: R$127,50 | Produtividade: 70 sacas
    Breakeven: 66.67 | Lucro = (70 - 66.67) * 127.50 = R$424.58
    """
    from app.repositories.cost_entry_repository import CostEntryRepository
    from app.schemas.cost_entry import CostEntryCreate

    repo = CostEntryRepository(db_session)
    entry = repo.create(CostEntryCreate(
        crop_type="soja", seeds=1000.0, fertilizers=2000.0, defensivos=1500.0,
        labor=2500.0, fuel=800.0, maintenance=700.0,
    ))

    service = _make_service(db_session, mock_gateway)
    result = service.simulate(SimulationRequest(
        crop_type="soja", estimated_productivity=70.0, cost_entry_id=entry.id
    ))

    breakeven = 8500.0 / 127.50
    expected_profit = round((70.0 - breakeven) * 127.50, 2)
    assert result.profit_loss_per_hectare == expected_profit


def test_breakeven_milho(db_session, mock_gateway):
    """
    Preço milho mock: R$62,80/saca | Custo: R$5.000/ha
    Breakeven: 5000 / 62.80 = 79.62 sacas/ha
    """
    from app.repositories.cost_entry_repository import CostEntryRepository
    from app.schemas.cost_entry import CostEntryCreate

    repo = CostEntryRepository(db_session)
    entry = repo.create(CostEntryCreate(
        crop_type="milho", seeds=800.0, fertilizers=1500.0, defensivos=700.0,
        labor=1200.0, fuel=500.0, maintenance=300.0,
    ))

    service = _make_service(db_session, mock_gateway)
    result = service.simulate(SimulationRequest(
        crop_type="milho", estimated_productivity=80.0, cost_entry_id=entry.id
    ))

    assert result.market_price_per_sack == 62.80
    assert result.total_cost_per_hectare == 5000.0
    assert result.breakeven_sacks_per_hectare == round(5000.0 / 62.80, 2)


def test_breakeven_feijao(db_session, mock_gateway):
    """Preço feijão mock: R$295,00/saca"""
    from app.repositories.cost_entry_repository import CostEntryRepository
    from app.schemas.cost_entry import CostEntryCreate

    repo = CostEntryRepository(db_session)
    entry = repo.create(CostEntryCreate(
        crop_type="feijao", seeds=2000.0, fertilizers=3000.0, defensivos=1000.0,
        labor=2000.0, fuel=500.0, maintenance=500.0,
    ))

    service = _make_service(db_session, mock_gateway)
    result = service.simulate(SimulationRequest(
        crop_type="feijao", estimated_productivity=30.0, cost_entry_id=entry.id
    ))

    assert result.market_price_per_sack == 295.0
    assert result.total_cost_per_hectare == 9000.0
    expected_breakeven = round(9000.0 / 295.0, 2)
    assert result.breakeven_sacks_per_hectare == expected_breakeven


def test_erro_quando_preco_mercado_zero(db_session):
    """Preço = 0 deve lançar CommodityFetchError (guarda contra divisão por zero)."""
    from unittest.mock import AsyncMock, MagicMock

    from app.repositories.commodity_cache_repository import CommodityCacheRepository
    from app.repositories.cost_entry_repository import CostEntryRepository

    gateway = MagicMock()
    gateway.fetch_price = AsyncMock(return_value=0.0)

    cost_repo = CostEntryRepository(db_session)
    cache_repo = CommodityCacheRepository(db_session)

    # Força cache stale para que o gateway seja chamado
    cache_repo.upsert("soja", 0.0, "test")
    cache = cache_repo.get_by_crop_type("soja")
    from datetime import UTC, datetime, timedelta
    cache.fetched_at = datetime.now(UTC) - timedelta(hours=25)
    db_session.commit()

    cost_service = CostService(cost_repo)
    commodity_service = CommodityService(gateway, cache_repo)
    simulation_service = SimulationService(cost_service, commodity_service)

    with pytest.raises(CommodityFetchError):
        simulation_service.simulate(SimulationRequest(crop_type="soja", estimated_productivity=60.0))
