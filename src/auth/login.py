import requests
from src.config import API_BASE_URL

def login(email, password):
    response = requests.post(f"{API_BASE_URL}/auth/login", json={"email": email, "password": password})
    response.raise_for_status()
    return response.json()

def logout(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/auth/logout", headers=headers)
    response.raise_for_status()
    return response.status_code

def refresh_token(refresh_token):
    response = requests.post(f"{API_BASE_URL}/auth/refresh", json={"refresh_token": refresh_token})
    response.raise_for_status()
    return response.json()

def verify_email(token):
    response = requests.get(f"{API_BASE_URL}/auth/verify", params={"token": token})
    response.raise_for_status()
    return response.json()
