import requests
from collections import defaultdict
from datetime import datetime

SHOPIFY_DOMAIN = "homatics-tv.myshopify.com"
ACCESS_TOKEN = "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"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def fetch_orders():
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/2023-10/orders.json?status=any"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    orders = response.json().get("orders", [])
    return orders

def aggregate_orders(orders):
    summary = defaultdict(lambda: defaultdict(float))
    for o in orders:
        date_str = o["created_at"][:10]  # e.g., "2025-05-26"
        country = (o.get("shipping_address") or {}).get("country_code", "Unknown")
        total = float(o.get("total_price", 0))
        summary[date_str][country] += total
    return summary
