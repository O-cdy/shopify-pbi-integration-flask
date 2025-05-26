import requests
from collections import defaultdict
from datetime import datetime, timedelta
from config import SHOPIFY_DOMAIN, ACCESS_TOKEN, API_VERSION, START_DATE

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def fetch_orders():
    """拉取所有订单，含分页处理"""
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

def get_all_days(start_date, end_date):
    days = []
    current = start_date
    while current <= end_date:
        days.append(current.strftime("%Y/%m/%d"))
        current += timedelta(days=1)
    return days

def aggregate_orders(orders):
    """聚合订单数据，每天每国家都返回，即使为0"""
    summary = defaultdict(lambda: {"net_sales": 0.0, "orders": 0})
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_date = datetime.today()

    countries = set()

    for order in orders:
        created_raw = order.get("created_at", "")
        try:
            created_dt = datetime.strptime(created_raw[:10], "%Y-%m-%d")
        except ValueError:
            continue

        if created_dt < start_date:
            continue

        country = (order.get("shipping_address") or {}).get("country", "Unknown")
        countries.add(country)

        key = (country, created_dt.strftime("%Y/%m/%d"))
        summary[key]["net_sales"] += float(order.get("total_price", 0.0))
        summary[key]["orders"] += 1

    all_days = get_all_days(start_date, end_date)

    result = []
    for day in all_days:
        for country in countries:
            key = (country, day)
            metrics = summary.get(key, {"net_sales": 0.0, "orders": 0})
            result.append({
                "Shipping country": country,
                "Day": day,
                "Net sales": round(metrics["net_sales"], 2),
                "Orders": metrics["orders"]
            })

    return result
