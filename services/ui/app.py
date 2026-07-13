from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

CATALOG_URL = os.environ.get("CATALOG_URL", "http://localhost:5002")
CART_URL = os.environ.get("CART_URL", "http://localhost:5001")
CHECKOUT_URL = os.environ.get("CHECKOUT_URL", "http://localhost:5004")

USER = "demo-user"

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/")
def index():
    products = requests.get(f"{CATALOG_URL}/catalog", timeout=5).json()
    cart = requests.get(f"{CART_URL}/cart/{USER}", timeout=5).json()
    return render_template("index.html", products=products, cart=cart)

@app.route("/add/<int:product_id>", methods=["POST"])
def add(product_id):
    requests.post(f"{CART_URL}/cart/{USER}/add", json={"product_id": product_id, "qty": 1}, timeout=5)
    return redirect("/")

@app.route("/checkout", methods=["POST"])
def checkout():
    result = requests.post(f"{CHECKOUT_URL}/checkout/{USER}", timeout=10)
    if result.status_code != 201:
        error_msg = result.json().get("error", "Checkout failed")
        return f"<h1>Checkout failed</h1><p>{error_msg}</p><a href='/'>Back to store</a>", 400
    return render_template("receipt.html", order=result.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
