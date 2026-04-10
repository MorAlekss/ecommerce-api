import sys
sys.path.insert(0, '.')
from unittest.mock import patch, MagicMock
from src.orders.checkout import create_cart, add_to_cart, checkout
from src.orders.history import list_orders, get_order, cancel_order
from src.orders.returns import create_return, get_return


def test_create_cart():
    with patch('src.orders.checkout.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "cart1", "items": []}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = create_cart("token123")
        assert result["id"] == "cart1"

def test_add_to_cart():
    with patch('src.orders.checkout.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "cart1", "items": [{"product_id": "p1", "quantity": 2}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = add_to_cart("cart1", "token123", "p1", 2)
        assert len(result["items"]) == 1

def test_list_orders():
    with patch('src.orders.history.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"orders": [{"id": "o1"}], "total": 1}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = list_orders("token123")
        assert result["total"] == 1

def test_create_return():
    with patch('src.orders.returns.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "r1", "status": "pending"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = create_return("o1", "token123", [{"product_id": "p1", "quantity": 1}], "defective")
        assert result["status"] == "pending"
