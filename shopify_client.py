import requests
from collections import defaultdict
from datetime import datetime
from config import SHOPIFY_DOMAIN, ACCESS_TOKEN, API_VERSION

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def fetch_orders():
    orders = []

    # 定义当前财年时间范围：2025-04-01 ~ 今天
    fiscal_start = "2025-04-01T00:00:00Z"
    today = datetime.utcnow().strftime("%Y-%m-%dT23:59:59Z")

    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/orders.json?status=any&created_at_min={fiscal_start}&created_at_max={today}&limit=250"

    print(f"📡 请求 URL：{url}")

    while url:
        response = requests.get(url, headers=headers)
        print(f"📥 响应状态码：{response.status_code}")
        data = response.json()
        orders.extend(data.get("orders", []))

        # 分页控制
        link = response.headers.get("Link")
        if link and 'rel="next"' in link:
            url = link.split(";")[0].strip("<> ")
        else:
            url = None

    return orders

def aggregate_orders(orders):
    data = defaultdict(lambda: {"net_sales": 0.0, "orders": 0})
    for order in orders:
        if not order.get("shipping_address"):
            continue
        country = order["shipping_address"].get("country", "Unknown")
        day = order["created_at"][:10]
        key = (country, day)
        data[key]["net_sales"] += float(order["total_price"])
        data[key]["orders"] += 1
    results = []
    for (country, day), metrics in data.items():
        results.append({
            "Shipping country": country,
            "Day": datetime.strptime(day, "%Y-%m-%d").strftime("%Y/%m/%d"),
            "Net sales": round(metrics["net_sales"], 2),
            "Orders": metrics["orders"]
        })
    return results
