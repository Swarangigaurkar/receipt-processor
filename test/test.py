import pytest
from flask import json
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_process_receipt(client):
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
        ],
        "total": "35.35"
    }

    response = client.post('/receipts/process', data=json.dumps(receipt_data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'id' in response_data

    receipt_id = response_data['id']

    response = client.get(f'/receipts/{receipt_id}/points')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'points' in response_data

    expected_points = 28
    assert response_data['points'] == expected_points

def test_invalid_receipt(client):
    invalid_receipt_data = {
        "retailer": "",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [],
        "total": ""
    }

    response = client.post('/receipts/process', data=json.dumps(invalid_receipt_data), content_type='application/json')
    assert response.status_code == 400

def test_multiple_receipts(client):
    receipt_data_1 = {
        "retailer": "Walmart",
        "purchaseDate": "2023-05-15",
        "purchaseTime": "14:30",
        "items": [
            {"shortDescription": "Apple", "price": "0.75"},
            {"shortDescription": "Banana", "price": "0.25"}
        ],
        "total": "1.00"
    }

    receipt_data_2 = {
        "retailer": "BestBuy",
        "purchaseDate": "2023-05-15",
        "purchaseTime": "15:00",
        "items": [
            {"shortDescription": "Laptop", "price": "999.99"}
        ],
        "total": "999.99"
    }

    response = client.post('/receipts/process', data=json.dumps(receipt_data_1), content_type='application/json')
    assert response.status_code == 200
    response_data_1 = json.loads(response.data)
    receipt_id_1 = response_data_1['id']

    response = client.post('/receipts/process', data=json.dumps(receipt_data_2), content_type='application/json')
    assert response.status_code == 200
    response_data_2 = json.loads(response.data)
    receipt_id_2 = response_data_2['id']

    response = client.get(f'/receipts/{receipt_id_1}/points')
    assert response.status_code == 200
    points_data_1 = json.loads(response.data)
    assert 'points' in points_data_1
    assert points_data_1['points'] == 11

    response = client.get(f'/receipts/{receipt_id_2}/points')
    assert response.status_code == 200
    points_data_2 = json.loads(response.data)
    assert 'points' in points_data_2
    assert points_data_2['points'] == 10

def test_no_items(client):
    receipt_data = {
        "retailer": "Empty Store",
        "purchaseDate": "2023-05-15",
        "purchaseTime": "10:30",
        "items": [],
        "total": "0.00"
    }

    response = client.post('/receipts/process', data=json.dumps(receipt_data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'id' in response_data

    receipt_id = response_data['id']

    response = client.get(f'/receipts/{receipt_id}/points')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'points' in response_data
    assert response_data['points'] == 10  # 10 points for retailer name with 10 alphanumeric characters

def test_edge_cases(client):
    receipt_data = {
        "retailer": "EdgeCaseStore",
        "purchaseDate": "2023-05-15",
        "purchaseTime": "03:30",
        "items": [
            {"shortDescription": "Short", "price": "1.00"},
            {"shortDescription": "VeryVeryLongDescription", "price": "2.25"},
            {"shortDescription": "ExactLengthMultipleOf3", "price": "3.00"}
        ],
        "total": "6.25"
    }

    response = client.post('/receipts/process', data=json.dumps(receipt_data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'id' in response_data

    receipt_id = response_data['id']

    response = client.get(f'/receipts/{receipt_id}/points')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'points' in response_data

    # Calculation: 13 (retailer name) + 5 (multiple of 2 items) + 1 (multiple of 3 description) + 6 (odd day) + 10 (after 2pm, before 4pm) = 35 points
    expected_points = 35
    assert response_data['points'] == expected_points