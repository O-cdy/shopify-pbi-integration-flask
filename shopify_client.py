import requests
from collections import defaultdict
from datetime import datetime
from config import SHOPIFY_DOMAIN, ACCESS_TOKEN, API_VERSION, START_DATE, END_DATE

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def fetch_orders():
    """拉取 FY25 的订单（带过滤）"""
    orders = []
    page = 1
    start_iso = f"{START_DATE}T00:00:00Z"
    end_iso = f"{END_DATE}T23:59:59Z"
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/orders.json?status=any&created_at_min={start_iso}&created_at_max={end_iso}&limit=250"

    while url:
        print(f"🌐 Fetching page {page} from: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        new_orders = data.get("orders", [])
        print(f"  ↳ Retrieved {len(new_orders)} orders")
        orders.extend(new_orders)
        page += 1

        link = response.headers.get("Link")
        if link and 'rel="next"' in link:
            url = link.split(";")[0].strip("<> ")
        else:
            url = None

    print(f"📦 Total orders fetched in FY25: {len(orders)}")
    return orders

def aggregate_orders(orders):
    """聚合为：每天 x 国家 维度的净销售额 + 订单数"""
    summary = defaultdict(lambda: {"net_sales": 0.0, "orders": 0})

    for order in orders:
        created_raw = order.get("created_at", "")
        try:
            created_dt = datetime.strptime(created_raw[:10], "%Y-%m-%d")
        except ValueError:
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
        for (country, day), metrics in sorted(summary.items())
    ]

    print(f"📊 Aggregation complete. Found {len(result)} daily records.")
    return result
