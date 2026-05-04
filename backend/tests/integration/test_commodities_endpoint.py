BASE = "/api/v1/commodities"


def test_list_all_prices(client):
    response = client.get(BASE)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    crops = {item["crop_type"] for item in data}
    assert crops == {"soja", "milho", "feijao"}


def test_get_soja_price(client):
    response = client.get(f"{BASE}/soja")
    assert response.status_code == 200
    data = response.json()
    assert data["crop_type"] == "soja"
    assert data["price_per_sack"] == 127.50
    assert data["currency"] == "BRL"


def test_get_milho_price(client):
    response = client.get(f"{BASE}/milho")
    assert response.status_code == 200
    assert response.json()["price_per_sack"] == 62.80


def test_get_feijao_price(client):
    response = client.get(f"{BASE}/feijao")
    assert response.status_code == 200
    assert response.json()["price_per_sack"] == 295.0


def test_get_invalid_crop_returns_422(client):
    response = client.get(f"{BASE}/trigo")
    assert response.status_code == 422


def test_refresh_prices(client):
    response = client.post(f"{BASE}/refresh")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
