import logging

import requests

logger = logging.getLogger(__name__)
API_URL = "http://127.0.0.1:8000"


def fetch_records(endpoint, params=None):
    response = requests.get(
        f"{API_URL}{endpoint}", params=params, timeout=10
    )
    response.raise_for_status()
    records = response.json()
    logger.debug(f"Fetched {endpoint}: rows={len(records)}")
    return records