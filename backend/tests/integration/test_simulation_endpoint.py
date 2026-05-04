BASE_COSTS = "/api/v1/costs"
BASE_SIM = "/api/v1/simulation"

COST_PAYLOAD = {
    "crop_type": "soja",
    "seeds": 1000.0,
    "fertilizers": 2000.0,
    "defensivos": 1500.0,
    "labor": 2500.0,
    "fuel": 800.0,
    "maintenance": 700.0,
}


def test_simulation_sem_custo_salvo(client):
    response = client.post(BASE_SIM, json={"crop_type": "soja", "estimated_productivity": 60.0})
    assert response.status_code == 200
    data = response.json()
    assert data["crop_type"] == "soja"
    assert data["total_cost_per_hectare"] == 0.0
    assert data["breakeven_sacks_per_hectare"] == 0.0
    assert data["currency"] == "BRL"


def test_simulation_com_custo_salvo_retorna_breakeven_correto(client):
    cost = client.post(BASE_COSTS, json=COST_PAYLOAD).json()
    response = client.post(BASE_SIM, json={
        "crop_type": "soja",
        "estimated_productivity": 70.0,
        "cost_entry_id": cost["id"],
    })
    assert response.status_code == 200
    data = response.json()

    assert data["total_cost_per_hectare"] == 8500.0
    assert data["market_price_per_sack"] == 127.50
    expected_breakeven = round(8500.0 / 127.50, 2)
    assert data["breakeven_sacks_per_hectare"] == expected_breakeven


def test_simulation_viavel(client):
    cost = client.post(BASE_COSTS, json=COST_PAYLOAD).json()
    response = client.post(BASE_SIM, json={
        "crop_type": "soja",
        "estimated_productivity": 70.0,
        "cost_entry_id": cost["id"],
    })
    data = response.json()
    assert data["is_viable"] is True
    assert data["profit_loss_per_hectare"] > 0


def test_simulation_inviavel(client):
    cost = client.post(BASE_COSTS, json=COST_PAYLOAD).json()
    response = client.post(BASE_SIM, json={
        "crop_type": "soja",
        "estimated_productivity": 50.0,
        "cost_entry_id": cost["id"],
    })
    data = response.json()
    assert data["is_viable"] is False
    assert data["profit_loss_per_hectare"] < 0


def test_simulation_crop_type_invalido_retorna_422(client):
    response = client.post(BASE_SIM, json={"crop_type": "trigo", "estimated_productivity": 60.0})
    assert response.status_code == 422


def test_simulation_produtividade_zero_retorna_422(client):
    response = client.post(BASE_SIM, json={"crop_type": "soja", "estimated_productivity": 0.0})
    assert response.status_code == 422


def test_simulation_milho(client):
    milho_cost = {**COST_PAYLOAD, "crop_type": "milho",
                  "seeds": 800.0, "fertilizers": 1500.0, "defensivos": 700.0,
                  "labor": 1200.0, "fuel": 500.0, "maintenance": 300.0}
    cost = client.post(BASE_COSTS, json=milho_cost).json()
    response = client.post(BASE_SIM, json={
        "crop_type": "milho",
        "estimated_productivity": 80.0,
        "cost_entry_id": cost["id"],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["market_price_per_sack"] == 62.80
    assert data["total_cost_per_hectare"] == 5000.0
