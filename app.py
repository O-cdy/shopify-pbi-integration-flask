from flask import Flask, jsonify
from shopify_client import fetch_orders, aggregate_orders
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask App on Render. Use `/daily-sales` to see data."

@app.route("/daily-sales", methods=["GET"])
def daily_sales():
    try:
        print("🔍 Fetching orders...")
        orders = fetch_orders()
        print(f"✅ {len(orders)} orders fetched.")

        summary = aggregate_orders(orders)
        return jsonify(summary)
    except Exception as e:
        print(f"❌ Error in /daily-sales: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
