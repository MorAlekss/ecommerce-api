import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.utils.http import get, post, put, patch as http_patch, delete
from src.utils.middleware import authenticated_get, authenticated_post


@pytest.mark.asyncio
async def test_get():
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "value"}
    mock_response.raise_for_status.return_value = None

    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch('src.utils.http.httpx.AsyncClient', return_value=mock_client):
        result = await get("https://api.example.com/test")
        assert result["data"] == "value"


@pytest.mark.asyncio
async def test_post():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "123"}
    mock_response.raise_for_status.return_value = None

    mock_client = MagicMock()
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch('src.utils.http.httpx.AsyncClient', return_value=mock_client):
        result = await post("https://api.example.com/test", {"key": "value"})
        assert result["id"] == "123"


def test_authenticated_get():
    """middleware.py still uses requests (not yet migrated by other worker)"""
    with patch('src.utils.middleware.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "secure"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = authenticated_get("https://api.example.com/secure", "token123")
        assert result["data"] == "secure"
