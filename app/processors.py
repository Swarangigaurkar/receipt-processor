import math
from datetime import datetime
from models import Receipt, ReceiptResponse, PointsResponse

def calculate_total_points(receipt: Receipt) -> int:
    """
    Calculates total points using the ID and reciept and returns total points as JSON response in the format {'id':points}
    _summary_

    Args:
        receipt (Receipt): _description_

    Returns:
        int: _description_
    """
    total_points=0
    rules = [ calculate_points_retailer_name, 
             calculate_points_total_amount_integer,
             calculate_points_total_amount_multiple,
             calculate_points_every_two_items,
             calculate_points_description_length,
             calculate_points_purchase_date,
             calculate_points_purchase_time
             ] 
    
    for rule in rules:
        total_points+=rule(receipt)

    return total_points

def calculate_points_retailer_name(receipt: Receipt) -> int:
    """
    Rule 1 One point for every alphanumeric character in the retailer name
    _summary_
    Args:
        receipt (Receipt): _description_

    Returns:
        int: _description_
    """
    points=sum(char.isalnum() for char in receipt.retailer)
    return points

def calculate_points_total_amount_integer(receipt: Receipt) -> int:
    """
    Rule 2 50 points if the total is a round dollar amount with no cents.
    _summary_
    Args:
        receipt (Receipt): _description_

    Returns:
        int: _description_
    """
    points=0
    if float(receipt.total).is_integer():
        points=50 
    return points

def calculate_points_total_amount_multiple(receipt: Receipt) -> int:
    """
    Rule 3 25 points if the total is a multiple of 0.25.
    _summary_
    Args:
        receipt (Receipt): _description_

    Returns:
        int: _description_
    """
    points=0
    if float(receipt.total)%0.25==0:
        points=25
    return points

def calculate_points_every_two_items(receipt: Receipt) -> int:
    """
    Rule 4 5 points for every two items on the receipts.
    _summary_
    Args:
        receipt (Receipt): _description_

    Returns:
        int: _description_
    """
    points=(len(receipt.items)//2)*5
    return points

def calculate_points_description_length(receipt: Receipt) -> int:
    """
    Rule 5 If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    _summary_
    Args:
        receipt (Receipt): _description_

    Returns:
        int: _description_
    """
    points=0
    for item in receipt.items:
        if len(item.shortDescription)>0 and len(item.shortDescription.strip())%3==0:
            points+=math.ceil(float(item.price)*0.2)
    return points

def calculate_points_purchase_date(receipt: Receipt) -> int:
    """
    Rule 6 6 points if the day in the purchase date is odd.
    _summary_
    Args:
        receipt (Receipt): _description_

    Returns:
        int: _description_
    """
    points=0
    if int(receipt.purchaseDate.split('-')[2])%2==1:
        points=6
    return points

def calculate_points_purchase_time(receipt: Receipt) -> int:
    """
    Rule 7 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    _summary_
    Args:
        receipt (Receipt): _description_

    Returns:
        int: _description_
    """
    points=0
    purchase_time=datetime.strptime(receipt.purchaseTime, "%H:%M")
    if 14 <= purchase_time.hour < 16:
        points=10
    return points