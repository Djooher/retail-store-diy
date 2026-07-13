from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

ORDERS = {}

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/orders", methods=["POST"])
def create_order():
    order_id = str(uuid.uuid4())[:8]
    body = request.get_json()
    ORDERS[order_id] = body
    return jsonify({"order_id": order_id, **body}), 201

@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "not found"}), 404
    return jsonify(order), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
