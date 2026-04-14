import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.utils.http import get, post, put, patch as http_patch, delete
from src.utils.middleware import (
    authenticated_get, authenticated_post,
    authenticated_put, authenticated_delete,
    log_request,
)


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


def _make_async_client_mock():
    client = AsyncMock()
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=client)
    cm.__aexit__ = AsyncMock(return_value=None)
    return client, cm


@pytest.mark.asyncio
async def test_authenticated_get():
    client, cm = _make_async_client_mock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "secure"}
    mock_response.raise_for_status.return_value = None
    client.get = AsyncMock(return_value=mock_response)
    with patch('src.utils.middleware.httpx.AsyncClient', return_value=cm):
        result = await authenticated_get("https://api.example.com/secure", "token123")
        assert result["data"] == "secure"


@pytest.mark.asyncio
async def test_authenticated_post():
    client, cm = _make_async_client_mock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "456"}
    mock_response.raise_for_status.return_value = None
    client.post = AsyncMock(return_value=mock_response)
    with patch('src.utils.middleware.httpx.AsyncClient', return_value=cm):
        result = await authenticated_post("https://api.example.com/secure", "token123", data={"key": "value"})
        assert result["id"] == "456"


@pytest.mark.asyncio
async def test_authenticated_put():
    client, cm = _make_async_client_mock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"updated": True}
    mock_response.raise_for_status.return_value = None
    client.put = AsyncMock(return_value=mock_response)
    with patch('src.utils.middleware.httpx.AsyncClient', return_value=cm):
        result = await authenticated_put("https://api.example.com/secure/1", "token123", data={"key": "value"})
        assert result["updated"] is True


@pytest.mark.asyncio
async def test_authenticated_delete():
    client, cm = _make_async_client_mock()
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.raise_for_status.return_value = None
    client.delete = AsyncMock(return_value=mock_response)
    with patch('src.utils.middleware.httpx.AsyncClient', return_value=cm):
        result = await authenticated_delete("https://api.example.com/secure/1", "token123")
        assert result == 204


@pytest.mark.asyncio
async def test_log_request():
    client, cm = _make_async_client_mock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    client.request = AsyncMock(return_value=mock_response)
    with patch('src.utils.middleware.httpx.AsyncClient', return_value=cm):
        result = await log_request("get", "https://api.example.com/test")
        assert result.status_code == 200
