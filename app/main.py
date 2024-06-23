# app/main.py
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
    if id not in receipts_db:
        return jsonify({"detail": "Receipt not found"}), 404
    return jsonify(PointsResponse(points=receipts_db[id]).dict())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)