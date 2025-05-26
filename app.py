from flask import Flask, jsonify
from shopify_client import fetch_orders, aggregate_orders

app = Flask(__name__)

# @app.route("/daily-sales", methods=["GET"])
# def daily_sales():
#     orders = fetch_orders()
#     summary = aggregate_orders(orders)
#     return jsonify(summary)

@app.route("/daily-sales", methods=["GET"])
def daily_sales():
    try:
        print("🔍 开始获取订单...")
        orders = fetch_orders()
        print(f"✅ 获取到 {len(orders)} 个订单")

        print("🔍 开始聚合订单...")
        summary = aggregate_orders(orders)
        print(f"✅ 聚合完成，共 {len(summary)} 条记录")

        return jsonify(summary)
    except Exception as e:
        print(f"❌ Exception in /daily-sales: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Flask server starting...")
    app.run(debug=True)
