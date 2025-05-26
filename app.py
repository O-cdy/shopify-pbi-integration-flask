from flask import Flask, jsonify
from shopify_client import fetch_orders, aggregate_orders

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Shopify Daily Sales API is running."

@app.route("/daily-sales", methods=["GET"])
def daily_sales():
    try:
        orders = fetch_orders()
        summary = aggregate_orders(orders)
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
