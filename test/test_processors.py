import json
import os
import pytest
from app.models import Receipt, Item
from app.processors import (calculate_total_points, calculate_points_total_amount_multiple, calculate_points_description_length, 
calculate_points_every_two_items, calculate_points_purchase_date, calculate_points_purchase_time, calculate_points_retailer_name, calculate_points_total_amount_integer)

@pytest.fixture
def get_test_data_from_json():
    with open(os.path.join(os.path.dirname(__file__), '../examples/receipt1.json')) as f:
        receipt_data=json.load(f)
    items=[Item(**item) for item in receipt_data['items']]

    return Receipt(retailer=receipt_data['retailer'],
                   purchaseDate=receipt_data['purchaseDate'],
                   purchaseTime=receipt_data['purchaseTime'],
                   items=items,
                   total=receipt_data['total'])
    
def test_calculate_points_retailer_name(get_test_data_from_json):
    points=calculate_points_retailer_name(get_test_data_from_json)
    assert points==6

def test_calculate_points_total_amount_integer(get_test_data_from_json):
    points=calculate_points_total_amount_integer(get_test_data_from_json)
    assert points==0

def test_calculate_points_total_amount_multiple(get_test_data_from_json):
    points=calculate_points_total_amount_multiple(get_test_data_from_json)
    assert points==0

def test_calculate_points_every_two_items(get_test_data_from_json):
    points=calculate_points_every_two_items(get_test_data_from_json)
    assert points==10

def test_calculate_points_description_length(get_test_data_from_json):
    points=calculate_points_description_length(get_test_data_from_json)
    assert points==6

def test_calculate_points_purchase_date(get_test_data_from_json):
    points=calculate_points_purchase_date(get_test_data_from_json)
    assert points==6

def test_calculate_points_purchase_time(get_test_data_from_json):
    points=calculate_points_purchase_time(get_test_data_from_json)
    assert points==0

def test_calculate_total_points(get_test_data_from_json):
    points=calculate_total_points(get_test_data_from_json)
    assert points==28