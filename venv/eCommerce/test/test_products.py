from jose import jwt
from app.domain.services.security import  secret_key

def test_register_product(client):
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/products/register", headers=headers, json={
        "code": "4152635",
        "name": "Guantes",
        "description": "Guantes rojos",
        "cost": 5,
        "margin": 30
    })
    assert response.status_code == 200
    assert response.json()["code"] == "4152635"

def test_get_products(client):
    response = client.get("/product")
    assert response.status_code == 200

def test_update_product(client):
    product_code = "wat56"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(f"/product/{product_code}", headers=headers, json={
                "code": "wat56",
                "name": "Smartwatch NovaTech Fit ",
                "description": "Smartwatch con GPS integrado y monitor de frecuencia cardíaca",
                "cost": 179.5,
                "margin": 13.7
    })
    assert response.status_code == 200
    assert response.json()["code"] == product_code

def test_get_product(client):
    product_code = "con65"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/product/{product_code}", headers=headers)

    assert response.status_code == 200
    assert response.json()["code"] == product_code

def test_delete_product(client):
    product_code = "cam43"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/delete/{product_code}", headers=headers)
    
    assert response.status_code == 200
