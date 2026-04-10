import sys
sys.path.insert(0, '.')
from unittest.mock import patch, MagicMock
from src.products.catalog import list_products, get_product, create_product, update_product
from src.products.search import search_products, get_suggestions
from src.products.inventory import get_stock, update_stock, reserve_stock


def test_list_products():
    with patch('src.products.catalog.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"products": [{"id": "p1"}, {"id": "p2"}], "total": 2}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = list_products()
        assert result["total"] == 2

def test_get_product():
    with patch('src.products.catalog.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "p1", "name": "Widget", "price": 9.99}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = get_product("p1")
        assert result["name"] == "Widget"

def test_search_products():
    with patch('src.products.search.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": [{"id": "p1", "name": "Widget"}], "total": 1}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = search_products("widget")
        assert result["total"] == 1

def test_get_stock():
    with patch('src.products.inventory.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"product_id": "p1", "quantity": 50}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = get_stock("p1", "token123")
        assert result["quantity"] == 50
