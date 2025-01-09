from jose import jwt
from app.domain.services.security import  secret_key

def test_register_cart(client):
    token = jwt.encode({"sub": "david"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/carts/register", headers=headers)
    assert response.status_code == 200

def test_get_cart(client):
    token = jwt.encode({"sub": "oriana"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/carts", headers=headers)
    assert response.status_code == 200


def test_register_product_cart(client):
    product_id = "1ccd13b6-299e-43f4-8f5d-bed4cccef296"
    token = jwt.encode({"sub": "oriana"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f"/carts/items/register/{product_id}", headers=headers, json={
          "quantity": 5

    })
    assert response.status_code == 200
    assert response.json()["product_id"] == product_id

def test_update_cart_item(client):
    product_id = "2ed14290-2c5c-47d1-b04d-a2c5bb6e10be"
    token = jwt.encode({"sub": "oriana"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/items/{product_id}", headers=headers, json={
          "quantity": 4
    })
    assert response.status_code == 200
    assert response.json()["product_id"] == product_id

def test_delete_product_cart(client):
    product_id = "09848c4e-b70b-4256-8fee-3b9a6d9f81ac"
    token = jwt.encode({"sub": "oriana"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/items/{product_id}", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["product_id"] == "09848c4e-b70b-4256-8fee-3b9a6d9f81ac"

