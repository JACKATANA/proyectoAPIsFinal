from jose import jwt
from app.domain.services.security import  secret_key

def test_register_orders(client):
    token = jwt.encode({"sub": "belen"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/orders", headers=headers)
    assert response.status_code == 200

def test_get_orders_client(client):
    user_id = "08740eec-7d0d-42e1-84b8-85fa4151996a"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/orders/{user_id}", headers=headers)

    assert response.status_code == 200

def test_get_order(client):
    order_id = "ac5e9453-52de-4caf-b9bd-e6e19543a59e"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/order/{order_id}", headers=headers)

    assert response.status_code == 200

def test_update_orders(client):
    order_id = "ac5e9453-52de-4caf-b9bd-e6e19543a59e"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/orders/{order_id}", headers=headers, json={
        "status": "completed",
    })
    assert response.status_code == 200
