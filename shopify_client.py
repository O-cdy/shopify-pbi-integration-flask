import requests
from collections import defaultdict
from datetime import datetime
from config import SHOPIFY_DOMAIN, ACCESS_TOKEN, API_VERSION, START_DATE

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def fetch_orders():
    """拉取所有订单（含分页）"""
    orders = []
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/orders.json?status=any&limit=250"
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        orders.extend(data.get("orders", []))

        link = response.headers.get("Link")
        if link and 'rel="next"' in link:
            url = link.split(";")[0].strip("<> ")
        else:
            url = None
    return orders

def aggregate_orders(orders):
    """聚合订单数据（只返回有销售或订单的行）"""
    summary = defaultdict(lambda: {"net_sales": 0.0, "orders": 0})
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")

    for order in orders:
        created_raw = order.get("created_at", "")
        try:
            created_dt = datetime.strptime(created_raw[:10], "%Y-%m-%d")
        except ValueError:
            continue
        if created_dt < start_date:
            continue

        country = (order.get("shipping_address") or {}).get("country", "Unknown")
        key = (country, created_dt.strftime("%Y/%m/%d"))
        summary[key]["net_sales"] += float(order.get("total_price", 0.0))
        summary[key]["orders"] += 1

    result = [
        {
            "Shipping country": country,
            "Day": day,
            "Net sales": round(metrics["net_sales"], 2),
            "Orders": metrics["orders"]
        }
        for (country, day), metrics in summary.items()
        if metrics["net_sales"] > 0 or metrics["orders"] > 0
    ]

    return result
