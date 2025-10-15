import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

ITEMS_PREFIX = "/api/v1/items"
ITEMS_INGEST = f"{ITEMS_PREFIX}/ingest"
