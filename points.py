from datetime import datetime
import math
import re

def calculate_points(receipt):
    """Calculate points for a receipt based on the rules in README.md."""
    points = 0

    # Rule 1: One point for every alphanumeric character in retailer name
    retailer = receipt['retailer']
    alphanumeric_chars = len(re.findall(r'[a-zA-Z0-9]', retailer))
    points += alphanumeric_chars

    # Rule 2: 50 points if total is a round dollar amount (no cents)
    total = float(receipt['total'])
    if total.is_integer():
        points += 50

    # Rule 3: 25 points if total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items
    items = receipt['items']
    points += (len(items) // 2) * 5

    # Rule 5: Points for item descriptions with trimmed length multiple of 3
    for item in items:
        description = item['shortDescription'].strip()
        if len(description) % 3 == 0:
            price = float(item['price'])
            points += math.ceil(price * 0.2)

    # Rule 6: 6 points if the day in purchase date is odd
    purchase_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
    if purchase_date.day % 2 != 0:
        points += 6

    # Rule 7: 10 points if purchase time is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt['purchaseTime'], '%H:%M')
    start_time = datetime.strptime('14:00', '%H:%M')
    end_time = datetime.strptime('16:00', '%H:%M')
    if start_time < purchase_time < end_time:
        points += 10

    return points