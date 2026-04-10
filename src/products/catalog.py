import requests
from src.config import API_BASE_URL

def list_products(page=1, limit=20, category=None, sort=None):
    params = {"page": page, "limit": limit}
    if category:
        params["category"] = category
    if sort:
        params["sort"] = sort
    response = requests.get(f"{API_BASE_URL}/products", params=params)
    response.raise_for_status()
    return response.json()

def get_product(product_id):
    response = requests.get(f"{API_BASE_URL}/products/{product_id}")
    response.raise_for_status()
    return response.json()

def create_product(token, data):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/products", json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def update_product(product_id, token, data):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{API_BASE_URL}/products/{product_id}", json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def delete_product(product_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL}/products/{product_id}", headers=headers)
    response.raise_for_status()
    return response.status_code
