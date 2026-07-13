from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Wireess Mouse", "price": 15.99},
    {"id": 2, "name": "Mechanical Keyboard", "price": 49.99},
    {"id": 3, "name": "USB-C Hub", "price": 22.50},
    {"id": 4, "name": "Webcam HD", "price": 34.00},
]

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/catalog")
def get_catalog():
    return jsonify(PRODUCTS), 200

@app.route("/catalog/<int:product_id>")
def get_product(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "not found"}), 404
    return jsonify(product), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
