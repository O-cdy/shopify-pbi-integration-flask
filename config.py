import os
from datetime import datetime
SHOPIFY_DOMAIN = os.environ.get("SHOPIFY_DOMAIN")
ACCESS_TOKEN = os.environ.get("SHOPIFY_TOKEN")
API_VERSION = os.environ.get("API_VERSION")
START_DATE = os.environ.get("START_DATE")
END_DATE = datetime.utcnow().strftime("%Y-%m-%dT23:59:59Z")


