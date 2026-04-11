import sys
import pytest
sys.path.insert(0, '.')
from unittest.mock import patch, AsyncMock, MagicMock
from src.utils.http import get, post, put, patch as http_patch, delete
from src.utils.middleware import authenticated_get, authenticated_post


@pytest.mark.asyncio
async def test_get():
    with patch('src.utils.http.httpx.AsyncClient') as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "value"}
        mock_response.raise_for_status.return_value = None
        mock_client.get.return_value = mock_response
        result = await get("https://api.example.com/test")
        assert result["data"] == "value"

@pytest.mark.asyncio
async def test_post():
    with patch('src.utils.http.httpx.AsyncClient') as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123"}
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value = mock_response
        result = await post("https://api.example.com/test", {"key": "value"})
        assert result["id"] == "123"

@pytest.mark.asyncio
async def test_authenticated_get():
    with patch('src.utils.middleware.httpx.AsyncClient') as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "secure"}
        mock_response.raise_for_status.return_value = None
        mock_client.get.return_value = mock_response
        result = await authenticated_get("https://api.example.com/secure", "token123")
        assert result["data"] == "secure"
