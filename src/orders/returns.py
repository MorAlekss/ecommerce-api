import requests
from src.config import API_BASE_URL

def create_return(order_id, token, items, reason):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/orders/{order_id}/returns",
                             json={"items": items, "reason": reason}, headers=headers)
    response.raise_for_status()
    return response.json()

def get_return(return_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/returns/{return_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def list_returns(token, page=1, limit=20):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": page, "limit": limit}
    response = requests.get(f"{API_BASE_URL}/returns", params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def approve_return(return_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(f"{API_BASE_URL}/returns/{return_id}",
                              json={"status": "approved"}, headers=headers)
    response.raise_for_status()
    return response.json()
