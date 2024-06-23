import math

def calculate_total_points(receipt: Receipt) -> int:
    total_points=0
    rules = ['calculate_points_retailer_name',
             'calculate_points_total_amount_integer',
             'calculate_points_total_amount_multiple',
             'calculate_points_every_two_items',
             'calculate_points_description_length',
             'calculate_points_purchase_date',
             'calculate_points_purchase_time'
             ] 
    
    for rule in rules:
        total_points+=rule(receipt)

    return total_points

def calculate_points_retailer_name(receipt: Receipt) -> int:
    points=sum(char.isalnum() for char in receipt.retailer)
    return points

def calculate_points_total_amount_integer(receipt: Receipt) -> int:
    points=0
    if float(receipt.total).is_integer():
        points=50 
    return points

def calculate_points_total_amount_multiple(receipt: Receipt) -> int:
    points=0
    if float(receipt.total)%0.25==0:
        points=25
    return points

def calculate_points_every_two_items(receipt: Receipt) -> int:
    points=(len(receipt.items)//2)*5
    return points

def calculate_points_description_length(receipt: Receipt) -> int:
    points=0
    for item in receipt.items:
        if len(item.shortDescription)>0 and len(item.shortDescription.strip())%3==0:
            points+=int(float(item.price)*0.2)
    return points

def calculate_points_purchase_date(receipt: Receipt) -> int:
    points=0
    if int(receipt.purchaseDate.split('-')[2])%2==1:
        points=6
    return points

def calculate_points_purchase_time(receipt: Receipt) -> int:
    points=0
    purchase_time=datetime.strptime(receipt.purchaseTime, "%H:%M")
    if 14 <= purchase_time.hour < 16:
        points=10
    return points