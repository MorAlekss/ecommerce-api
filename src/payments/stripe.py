import requests
from src.config import API_BASE_URL, STRIPE_SECRET_KEY

STRIPE_BASE = "https://api.stripe.com/v1"
STRIPE_HEADERS = {"Authorization": f"Bearer {STRIPE_SECRET_KEY}"}

def create_payment_intent(amount, currency, metadata=None):
    data = {"amount": amount, "currency": currency}
    if metadata:
        for k, v in metadata.items():
            data[f"metadata[{k}]"] = v
    response = requests.post(f"{STRIPE_BASE}/payment_intents", data=data, headers=STRIPE_HEADERS)
    response.raise_for_status()
    return response.json()

def confirm_payment(payment_intent_id, payment_method_id):
    response = requests.post(f"{STRIPE_BASE}/payment_intents/{payment_intent_id}/confirm",
                             data={"payment_method": payment_method_id}, headers=STRIPE_HEADERS)
    response.raise_for_status()
    return response.json()

def refund_payment(payment_intent_id, amount=None):
    data = {"payment_intent": payment_intent_id}
    if amount:
        data["amount"] = amount
    response = requests.post(f"{STRIPE_BASE}/refunds", data=data, headers=STRIPE_HEADERS)
    response.raise_for_status()
    return response.json()

def get_payment(payment_intent_id):
    response = requests.get(f"{STRIPE_BASE}/payment_intents/{payment_intent_id}", headers=STRIPE_HEADERS)
    response.raise_for_status()
    return response.json()
