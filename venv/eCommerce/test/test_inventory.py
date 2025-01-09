from jose import jwt
from app.domain.services.security import  secret_key

def test_register_inventory(client):
    product_id = "04c9aeab-39b1-4095-8386-18b6e15e0029"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f"/inventories/{product_id}", headers=headers, json={
                "product_id": "04c9aeab-39b1-4095-8386-18b6e15e0029",
                "quantity": 4000

    })
    assert response.status_code == 200
    assert response.json()["product_id"] == "04c9aeab-39b1-4095-8386-18b6e15e0029"

def test_update_inventory(client):
    product_id = "2ed14290-2c5c-47d1-b04d-a2c5bb6e10be"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/inventories/{product_id}", headers=headers, json={
                "product_id": "2ed14290-2c5c-47d1-b04d-a2c5bb6e10be",
                "quantity": 5000

    })
    assert response.status_code == 200
    assert response.json()["product_id"] =="2ed14290-2c5c-47d1-b04d-a2c5bb6e10be"

def test_get_inventory(client):
    product_id = "21cf8d12-1ffd-4bfc-90a8-e4b25945e5c5"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/inventories/{product_id}", headers=headers)
    assert response.status_code == 200