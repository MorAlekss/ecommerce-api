import requests
from src.config import API_BASE_URL

def create_cart(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/cart", headers=headers)
    response.raise_for_status()
    return response.json()

def add_to_cart(cart_id, token, product_id, quantity):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/cart/{cart_id}/items",
                             json={"product_id": product_id, "quantity": quantity}, headers=headers)
    response.raise_for_status()
    return response.json()

def remove_from_cart(cart_id, item_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL}/cart/{cart_id}/items/{item_id}", headers=headers)
    response.raise_for_status()
    return response.status_code

def checkout(cart_id, token, payment_method, shipping_address):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/cart/{cart_id}/checkout",
                             json={"payment_method": payment_method, "shipping_address": shipping_address},
                             headers=headers)
    response.raise_for_status()
    return response.json()
