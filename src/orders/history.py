import requests
from src.config import API_BASE_URL

def list_orders(token, page=1, limit=20, status=None):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "limit": limit}
    if status:
        params["status"] = status
    response = requests.get(f"{API_BASE_URL}/orders", params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def get_order(order_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/orders/{order_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def get_order_tracking(order_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/orders/{order_id}/tracking", headers=headers)
    response.raise_for_status()
    return response.json()

def cancel_order(order_id, token, reason):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/orders/{order_id}/cancel",
                             json={"reason": reason}, headers=headers)
    response.raise_for_status()
    return response.json()
