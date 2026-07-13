from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

CART_URL = os.environ.get("CART_URL", "http://localhost:5001")
CATALOG_URL = os.environ.get("CATALOG_URL", "http://localhost:5002")
ORDERS_URL = os.environ.get("ORDERS_URL", "http://localhost:5003")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/checkout/<user_id>", methods=["POST"])
def checkout(user_id):
    cart_resp = requests.get(f"{CART_URL}/cart/{user_id}", timeout=5)
    cart_items = cart_resp.json()

    if not cart_items:
        return jsonify({"error": "cart is empty"}), 400

    total = 0
    line_items = []
    for item in cart_items:
        product_resp = requests.get(f"{CATALOG_URL}/catalog/{item['product_id']}", timeout=5)
        if product_resp.status_code != 200:
            continue
        product = product_resp.json()
        qty = item.get("qty", 1)
        subtotal = product["price"] * qty
        total += subtotal
        line_items.append({"name": product["name"], "qty": qty, "subtotal": subtotal})

    order_resp = requests.post(
        f"{ORDERS_URL}/orders",
        json={"user_id": user_id, "line_items": line_items, "total": round(total, 2)},
        timeout=5,
    )
    order = order_resp.json()

    requests.post(f"{CART_URL}/cart/{user_id}/clear", timeout=5)

    return jsonify(order), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
