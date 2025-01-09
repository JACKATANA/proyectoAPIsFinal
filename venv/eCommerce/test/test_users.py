from jose import jwt
from app.domain.services.security import  secret_key

def test_register_user(client):
    response = client.post("/users/register", json={
        "username": "Cara",
        "email": "cara@example.com",
        "role": "customer",
        "password": "123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "cara@example.com"

def test_login_successful(client):
    form_data = {"username": "oriana", "password": "oriana"}
    response = client.post("/users/login", data=form_data)
    assert response.status_code == 200

def test_user_me_endpoint(client):
    token = jwt.encode({"sub": "oriana"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "oriana"
    assert response.json()["email"] == "oriana@example.com"

def test_register_superadmin(client):
    response = client.post("/users/create_superadmin", json={
        "username": "crismary",
        "email": "crismary@example.com",
        "role": "superadmin",
        "password": "crismary"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "crismary@example.com"

def test_register_manager(client):
    token = jwt.encode({"sub": "crismary"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/users/managers", headers=headers, json={
        "username": "angel",
        "email": "angel@example.com",
        "role": "manager",
        "password": "angel"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "angel@example.com"

def test_get_manager(client):
    token = jwt.encode({"sub": "crismary"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/managers", headers=headers)
    assert response.status_code == 200

def test_update_manager(client):
    manager_id = "3262c467-73cc-4ffe-a661-7de73c675a42"
    token = jwt.encode({"sub": "crismary"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/users/managers/{manager_id}", headers=headers, json={
        "username": "alex",
        "email": "alex@example.com",
        "role": "manager",
        "password": "alex"
    })
    assert response.status_code == 200

def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200

def test_update_customer(client):
    user_id = "b8c953f1-e2f2-41c5-a086-a99be5afe26c"
    token = jwt.encode({"sub": "crismary"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/users/{user_id}", headers=headers, json={
        "username": "tahma",
        "email": "tahma@example.com",
        "role": "customer",
        "password": "tahma"
    })
    assert response.status_code == 200

def test_delete_manager(client):
    manager_id = "70c0876a-73c4-4f75-8519-0d75da75f901"
    token = jwt.encode({"sub": "crismary"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/user/managers/{manager_id}", headers=headers)
    
    assert response.status_code == 200
