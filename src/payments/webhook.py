import requests
from src.config import API_BASE_URL

def register_webhook(token, url, events):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/webhooks",
                             json={"url": url, "events": events}, headers=headers)
    response.raise_for_status()
    return response.json()

def list_webhooks(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/webhooks", headers=headers)
    response.raise_for_status()
    return response.json()

def delete_webhook(webhook_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{API_BASE_URL}/webhooks/{webhook_id}", headers=headers)
    response.raise_for_status()
    return response.status_code

def test_webhook(webhook_id, token, event_type):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/webhooks/{webhook_id}/test",
                             json={"event_type": event_type}, headers=headers)
    response.raise_for_status()
    return response.json()
