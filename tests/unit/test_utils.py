import sys
sys.path.insert(0, '.')
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from src.utils.http import get, post, put, patch as http_patch, delete
from src.utils.middleware import authenticated_get, authenticated_post


def test_get():
    with patch('src.utils.http.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "value"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = get("https://api.example.com/test")
        assert result["data"] == "value"

def test_post():
    with patch('src.utils.http.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = post("https://api.example.com/test", {"key": "value"})
        assert result["id"] == "123"

@pytest.mark.asyncio
async def test_authenticated_get():
    with patch('src.utils.middleware.httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "secure"}
        mock_response.raise_for_status.return_value = None
        mock_instance = MagicMock()
        mock_instance.get = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_instance
        result = await authenticated_get("https://api.example.com/secure", "token123")
        assert result["data"] == "secure"

@pytest.mark.asyncio
async def test_authenticated_post():
    with patch('src.utils.middleware.httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "456"}
        mock_response.raise_for_status.return_value = None
        mock_instance = MagicMock()
        mock_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_instance
        result = await authenticated_post("https://api.example.com/items", "token123", data={"name": "test"})
        assert result["id"] == "456"
