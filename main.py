from flask import Flask, request, jsonify
import uuid
import re
from datetime import datetime
from points import calculate_points
import hashlib
import json

app = Flask(__name__)

# In-memory storage for receipts
receipts = {}
receipt_hashes = {}

def hash_receipt(receipt):
    """Compute a stable hash of the receipt."""
    normalized = json.dumps(receipt, sort_keys=True)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

def validate_receipt(receipt):
    """Validate receipt against schema defined in api.yml."""
    # Required fields
    required_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
    for field in required_fields:
        if field not in receipt:
            return False, f"Missing required field: {field}"

    # Validate retailer: ^[\w\s\-&]+$
    if not re.match(r'^[\w\s\-&]+$', receipt['retailer']):
        return False, "Invalid retailer format"

    # Validate purchaseDate: YYYY-MM-DD
    try:
        datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
    except ValueError:
        return False, "Invalid purchaseDate format"

    # Validate purchaseTime: HH:MM (24-hour)
    try:
        datetime.strptime(receipt['purchaseTime'], '%H:%M')
    except ValueError:
        return False, "Invalid purchaseTime format"

    # Validate items: Array with at least 1 item
    if not isinstance(receipt['items'], list) or len(receipt['items']) < 1:
        return False, "Items must be a non-empty array"

    # Validate each item
    for item in receipt['items']:
        if not all(key in item for key in ['shortDescription', 'price']):
            return False, "Item missing shortDescription or price"
        # Validate shortDescription: ^[\w\s\-]+$
        if not re.match(r'^[\w\s\-]+$', item['shortDescription']):
            return False, "Invalid item shortDescription format"
        # Validate price: ^\d+\.\d{2}$
        if not re.match(r'^\d+\.\d{2}$', item['price']):
            return False, "Invalid item price format"

    # Validate total: ^\d+\.\d{2}$
    if not re.match(r'^\d+\.\d{2}$', receipt['total']):
        return False, "Invalid total format"

    return True, ""

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """Process a receipt and return a unique ID."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    receipt = request.get_json()
    is_valid, error_message = validate_receipt(receipt)
    if not is_valid:
        return jsonify({"error": f"The receipt is invalid. {error_message}"}), 400
    
    # Compute hash of the receipt
    receipt_hash = hash_receipt(receipt)

    # Check if already exists
    if receipt_hash in receipt_hashes:
        existing_id = receipt_hashes[receipt_hash]
        return jsonify({"id": existing_id}), 200

    # Generate unique ID
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = receipt
    receipt_hashes[receipt_hash] = receipt_id

    return jsonify({"id": receipt_id}), 200

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    """Return the points awarded for a receipt by ID."""
    if id not in receipts:
        return jsonify({"error": "No receipt found for that ID."}), 404

    receipt = receipts[id]
    points = calculate_points(receipt)
    return jsonify({"points": points}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)