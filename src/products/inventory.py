import requests
from src.config import API_BASE_URL

def get_stock(product_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/products/{product_id}/inventory", headers=headers)
    response.raise_for_status()
    return response.json()

def update_stock(product_id, token, quantity, warehouse=None):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"quantity": quantity}
    if warehouse:
        data["warehouse"] = warehouse
    response = requests.patch(f"{API_BASE_URL}/products/{product_id}/inventory",
                              json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def reserve_stock(product_id, token, quantity, order_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/products/{product_id}/inventory/reserve",
                             json={"quantity": quantity, "order_id": order_id}, headers=headers)
    response.raise_for_status()
    return response.json()

def release_stock(product_id, token, order_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL}/products/{product_id}/inventory/reserve/{order_id}",
                               headers=headers)
    response.raise_for_status()
    return response.status_code
