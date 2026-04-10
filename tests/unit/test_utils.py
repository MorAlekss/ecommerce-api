import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.utils.http import get, post, put, patch as http_patch, delete
from src.utils.middleware import authenticated_get, authenticated_post


def _make_async_client_mock():
    """Helper to create a properly mocked httpx.AsyncClient context manager."""
    client = AsyncMock()
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=client)
    cm.__aexit__ = AsyncMock(return_value=None)
    return client, cm


@pytest.mark.asyncio
async def test_get():
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "value"}
    mock_response.raise_for_status.return_value = None
    client, cm = _make_async_client_mock()
    client.get = AsyncMock(return_value=mock_response)
    with patch('src.utils.http.httpx.AsyncClient', return_value=cm):
        result = await get("https://api.example.com/test")
        assert result["data"] == "value"


@pytest.mark.asyncio
async def test_post():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "123"}
    mock_response.raise_for_status.return_value = None
    client, cm = _make_async_client_mock()
    client.post = AsyncMock(return_value=mock_response)
    with patch('src.utils.http.httpx.AsyncClient', return_value=cm):
        result = await post("https://api.example.com/test", {"key": "value"})
        assert result["id"] == "123"


@pytest.mark.asyncio
async def test_authenticated_get():
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "secure"}
    mock_response.raise_for_status.return_value = None
    client, cm = _make_async_client_mock()
    client.get = AsyncMock(return_value=mock_response)
    with patch('src.utils.middleware.httpx.AsyncClient', return_value=cm):
        result = await authenticated_get("https://api.example.com/secure", "token123")
        assert result["data"] == "secure"


@pytest.mark.asyncio
async def test_authenticated_post():
    mock_response = MagicMock()
    mock_response.json.return_value = {"created": True}
    mock_response.raise_for_status.return_value = None
    client, cm = _make_async_client_mock()
    client.post = AsyncMock(return_value=mock_response)
    with patch('src.utils.middleware.httpx.AsyncClient', return_value=cm):
        result = await authenticated_post("https://api.example.com/data", "token123", {"key": "val"})
        assert result["created"] is True
