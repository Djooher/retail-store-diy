from flask import Flask, jsonify, request

app = Flask(__name__)

CARTS = {}

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/cart/<user_id>", methods=["GET"])
def get_cart(user_id):
    return jsonify(CARTS.get(user_id, [])), 200

@app.route("/cart/<user_id>/add", methods=["POST"])
def add_to_cart(user_id):
    item = request.get_json()
    CARTS.setdefault(user_id, []).append(item)
    return jsonify(CARTS[user_id]), 201

@app.route("/cart/<user_id>/clear", methods=["POST"])
def clear_cart(user_id):
    CARTS[user_id] = []
    return jsonify([]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
