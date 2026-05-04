from datetime import UTC, datetime, timedelta

import pytest

from app.gateways.mock_commodity_gateway import MockCommodityGateway
from app.repositories.commodity_cache_repository import CommodityCacheRepository
from app.services.commodity_service import CommodityService


@pytest.fixture
def service(db_session):
    gateway = MockCommodityGateway(randomize=False)
    cache_repo = CommodityCacheRepository(db_session)
    return CommodityService(gateway, cache_repo)


def test_get_price_soja_retorna_valor_correto(service):
    result = service.get_price("soja")
    assert result.crop_type == "soja"
    assert result.price_per_sack == 127.50
    assert result.currency == "BRL"


def test_get_price_salva_no_cache(service, db_session):
    service.get_price("milho")
    cache_repo = CommodityCacheRepository(db_session)
    cached = cache_repo.get_by_crop_type("milho")

    assert cached is not None
    assert float(cached.price_per_sack) == 62.80


def test_get_price_usa_cache_quando_fresco(db_session):
    cache_repo = CommodityCacheRepository(db_session)
    cache_repo.upsert("feijao", 999.99, "test_cache")

    gateway = MockCommodityGateway(randomize=False)
    service = CommodityService(gateway, cache_repo)
    result = service.get_price("feijao")

    assert result.price_per_sack == 999.99


def test_get_price_busca_api_quando_cache_stale(db_session):
    cache_repo = CommodityCacheRepository(db_session)
    cache_repo.upsert("soja", 50.0, "old_source")

    stale = cache_repo.get_by_crop_type("soja")
    stale.fetched_at = datetime.now(UTC) - timedelta(hours=25)
    db_session.commit()

    gateway = MockCommodityGateway(randomize=False)
    service = CommodityService(gateway, cache_repo)
    result = service.get_price("soja")

    assert result.price_per_sack == 127.50


def test_get_all_prices_retorna_tres_culturas(service):
    results = service.get_all_prices()
    crop_types = {r.crop_type for r in results}
    assert crop_types == {"soja", "milho", "feijao"}


def test_refresh_all_atualiza_cache(db_session):
    cache_repo = CommodityCacheRepository(db_session)
    gateway = MockCommodityGateway(randomize=False)
    service = CommodityService(gateway, cache_repo)

    results = service.refresh_all()
    assert len(results) == 3
