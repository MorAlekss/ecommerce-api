import requests
from src.config import API_BASE_URL

def get_oauth_url(provider, redirect_uri):
    response = requests.get(f"{API_BASE_URL}/auth/oauth/{provider}", params={"redirect_uri": redirect_uri})
    response.raise_for_status()
    return response.json()

def exchange_oauth_code(provider, code, redirect_uri):
    response = requests.post(f"{API_BASE_URL}/auth/oauth/{provider}/callback",
                             json={"code": code, "redirect_uri": redirect_uri})
    response.raise_for_status()
    return response.json()

def revoke_oauth_token(provider, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL}/auth/oauth/{provider}/revoke", headers=headers)
    response.raise_for_status()
    return response.status_code
