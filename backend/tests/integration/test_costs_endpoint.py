

BASE = "/api/v1/costs"

VALID_PAYLOAD = {
    "crop_type": "soja",
    "seeds": 1000.0,
    "fertilizers": 2000.0,
    "defensivos": 500.0,
    "labor": 1500.0,
    "fuel": 400.0,
    "maintenance": 600.0,
}


def test_create_cost_returns_201(client):
    response = client.post(BASE, json=VALID_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["crop_type"] == "soja"
    assert data["total_cost"] == 6000.0
    assert "id" in data


def test_create_cost_invalid_crop_type_returns_422(client):
    payload = {**VALID_PAYLOAD, "crop_type": "arroz"}
    response = client.post(BASE, json=payload)
    assert response.status_code == 422


def test_create_cost_negative_value_returns_422(client):
    payload = {**VALID_PAYLOAD, "seeds": -100.0}
    response = client.post(BASE, json=payload)
    assert response.status_code == 422


def test_create_cost_value_too_large_returns_422(client):
    payload = {**VALID_PAYLOAD, "fertilizers": 9_999_999.0}
    response = client.post(BASE, json=payload)
    assert response.status_code == 422


def test_list_costs_returns_200(client):
    client.post(BASE, json=VALID_PAYLOAD)
    response = client.get(BASE)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_cost_by_id(client):
    created = client.post(BASE, json=VALID_PAYLOAD).json()
    response = client.get(f"{BASE}/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_cost_not_found(client):
    response = client.get(f"{BASE}/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_cost_partial(client):
    created = client.post(BASE, json=VALID_PAYLOAD).json()
    response = client.put(f"{BASE}/{created['id']}", json={"seeds": 2000.0})
    assert response.status_code == 200
    assert response.json()["seeds"] == 2000.0
    assert response.json()["fertilizers"] == 2000.0


def test_delete_cost(client):
    created = client.post(BASE, json=VALID_PAYLOAD).json()
    response = client.delete(f"{BASE}/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"{BASE}/{created['id']}")
    assert response.status_code == 404
