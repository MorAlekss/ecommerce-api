import sys
sys.path.insert(0, '.')
from unittest.mock import patch, MagicMock
from src.payments.stripe import create_payment_intent, confirm_payment, refund_payment
from src.payments.webhook import register_webhook, list_webhooks, delete_webhook


def test_create_payment_intent():
    with patch('src.payments.stripe.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "pi_123", "status": "requires_payment_method"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = create_payment_intent(1000, "usd")
        assert result["id"] == "pi_123"

def test_refund_payment():
    with patch('src.payments.stripe.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "re_123", "status": "succeeded"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = refund_payment("pi_123")
        assert result["status"] == "succeeded"

def test_register_webhook():
    with patch('src.payments.webhook.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "wh_123", "url": "https://example.com/webhook"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = register_webhook("token123", "https://example.com/webhook", ["payment.success"])
        assert result["id"] == "wh_123"
