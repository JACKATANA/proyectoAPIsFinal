from jose import jwt
from app.domain.services.security import  secret_key

def test_report_sales_total(client):
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/reports/sales/total", headers=headers)
    assert response.status_code == 200

def test_report_sales_product(client):
    product_id="2ed14290-2c5c-47d1-b04d-a2c5bb6e10be"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/reports/sales/{product_id}", headers=headers)
    assert response.status_code == 200

def test_report_profit_total(client):
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/reports/profit/total", headers=headers)
    assert response.status_code == 200

def test_report_profit_product(client):
    producto_id="d3bd2c53-3a0d-4f90-8bbe-ef392df29903"
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/reports/profit/{producto_id}", headers=headers)
    assert response.status_code == 200

def test_report_customers_top(client):
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/customers/top", headers=headers)
    assert response.status_code == 200

def test_report_products_top(client):
    token = jwt.encode({"sub": "cris"}, secret_key, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/products/top", headers=headers)
    assert response.status_code == 200
