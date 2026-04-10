import requests
from src.config import API_BASE_URL

def search_products(query, filters=None, page=1, limit=20):
    params = {"q": query, "page": page, "limit": limit, **(filters or {})}
    response = requests.get(f"{API_BASE_URL}/products/search", params=params)
    response.raise_for_status()
    return response.json()

def get_suggestions(query, limit=5):
    response = requests.get(f"{API_BASE_URL}/products/suggestions", params={"q": query, "limit": limit})
    response.raise_for_status()
    return response.json()

def get_related_products(product_id, limit=10):
    response = requests.get(f"{API_BASE_URL}/products/{product_id}/related", params={"limit": limit})
    response.raise_for_status()
    return response.json()
