from flask import Flask, request, jsonify
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from models import Receipt, ReceiptResponse, PointsResponse
from processors import calculate_total_points

app = Flask(__name__)

receipts_db = {}

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    """
    Function handles POST requests to /receipts/process. 
    From the JSON payload, generates a unique id using uuid, calculates 
    points based on the receipt and stores the points with the id as the key.
    Returns the id as the JSON response.
    _summary_
    Returns:
        id (_type_) : uuid
    """
    try:
        receipt = Receipt(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    receipt_id = str(uuid4())
    points = calculate_total_points(receipt)
    receipts_db[receipt_id] = points
    return jsonify(ReceiptResponse(id=receipt_id).dict())

@app.route("/receipts/<id>/points", methods=["GET"])
def get_points(id):
    """
    Function handles GET requests to /receipts/<id>/points. 
    It returns points based on the receipt id as the JSON response.
    _summary_
    Args:
        id (_type_): uuid
    Returns:
        id : points
    """
    if id not in receipts_db:
        return jsonify({"detail": "Receipt not found"}), 404
    return jsonify(PointsResponse(points=receipts_db[id]).dict())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)