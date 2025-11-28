import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import date
import requests

client = TestClient(app)

def test_create_order_success(requests_mock):
    product_id = 1
    price = 100.0
    requests_mock.get(
        f"http://localhost:8080/products/{product_id}",
        json={"id": product_id, "price": price}
    )

    order_data = {
        "items": [{"product_id": product_id, "quantity": 2}]
    }

    response = client.post("/orders", json=order_data)

    assert response.status_code == 201
    data = response.json()
    assert data["total_amount"] == 200.0
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 2
    assert "delivery_date" in data
    assert date.fromisoformat(data["delivery_date"])

def test_create_order_product_not_found(requests_mock):
    product_id = 999
    requests_mock.get(
        f"http://localhost:8080/products/{product_id}",
        status_code=404
    )

    order_data = {
        "items": [{"product_id": product_id, "quantity": 1}]
    }

    response = client.post("/orders", json=order_data)

    assert response.status_code == 400
    assert f"Product with id {product_id} not found" in response.json()["detail"]

def test_create_order_service_unavailable(requests_mock):
    product_id = 1
    requests_mock.get(
        f"http://localhost:8080/products/{product_id}",
        exc=requests.exceptions.ConnectTimeout
    )

    order_data = {
        "items": [{"product_id": product_id, "quantity": 1}]
    }

    response = client.post("/orders", json=order_data)

    assert response.status_code == 503
    assert "unavailable" in response.json()["detail"]
