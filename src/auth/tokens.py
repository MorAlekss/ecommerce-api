import requests
from src.config import API_BASE_URL

def get_api_tokens(user_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/users/{user_id}/tokens", headers=headers)
    response.raise_for_status()
    return response.json()

def create_api_token(user_id, token, name, scopes):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/users/{user_id}/tokens",
                             json={"name": name, "scopes": scopes}, headers=headers)
    response.raise_for_status()
    return response.json()

def revoke_api_token(user_id, token_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL}/users/{user_id}/tokens/{token_id}", headers=headers)
    response.raise_for_status()
    return response.status_code
