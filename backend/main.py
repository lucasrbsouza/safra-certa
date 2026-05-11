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

_DESCRIPTION = """
## Visão Geral

**SafraCerta** é um simulador de viabilidade financeira para produtores rurais brasileiros.
Calcula o **ponto de equilíbrio** cruzando custos de produção reais com cotações de mercado
de commodities agrícolas (soja, milho, feijão).

## Fórmula Principal

```
ponto_equilíbrio (sc/ha) = custo_total_por_hectare (R$/ha) ÷ preço_por_saca (R$/sc)
```

A lavoura é **viável** quando `produtividade_estimada ≥ ponto_equilíbrio`.

## Fluxo de Uso

1. **Cadastre os custos** → `POST /api/v1/costs`
2. **Consulte as cotações** → `GET /api/v1/commodities`
3. **Execute a simulação** → `POST /api/v1/simulation`

## Notas

- Todos os valores monetários estão em **BRL (R$)**.
- Unidade de produção: **sacas de 60 kg por hectare (sc/ha)**.
- Cotações de mercado possuem **cache de 24 horas**.
- Validação OWASP: campos de custo aceitos no intervalo `[0, 1.000.000]`.
"""

_TAGS_METADATA = [
    {
        "name": "Costs",
        "description": (
            "Gerenciamento de registros de custo de produção por hectare. "
            "Cada entrada representa insumos, mão de obra e despesas operacionais de uma cultura."
        ),
    },
    {
        "name": "Market",
        "description": (
            "Cotações de mercado de commodities agrícolas em **R$/saca de 60 kg**. "
            "Dados com cache de 24 horas para evitar sobrecarga na API de origem."
        ),
    },
    {
        "name": "Simulation",
        "description": (
            "Motor de cálculo do ponto de equilíbrio. "
            "Retorna viabilidade financeira, margem estimada e resultado consolidado da lavoura."
        ),
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=_get_engine())
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="SafraCerta API",
        summary="Simulador de ponto de equilíbrio para produtores rurais brasileiros.",
        version="1.0.0",
        description=_DESCRIPTION,
        openapi_tags=_TAGS_METADATA,
        contact={
            "name": "Equipe SafraCerta",
            "email": "contato@safracerta.com.br",
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
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
