from flask import Flask, jsonify
from shopify_client import fetch_orders, aggregate_orders

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Shopify Daily Sales API is running."

@app.route("/daily-sales", methods=["GET"])
def daily_sales():
    try:
        print("📦 Fetching orders from Shopify...")
        orders = fetch_orders()
        print(f"✅ Fetched {len(orders)} orders.")

        print("📊 Aggregating order data...")
        summary = aggregate_orders(orders)
        print(f"✅ Aggregated into {len(summary)} country-day records.")

        return jsonify({"data": summary})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting Flask server on port {port}...")
    app.run(host="0.0.0.0", port=port)
