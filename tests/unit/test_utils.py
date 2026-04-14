import sys
sys.path.insert(0, '.')
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
import httpx
from src.utils.http import get, post, put, patch as http_patch, delete
from src.utils.middleware import authenticated_get, authenticated_post
from src.utils.retry import retry_request, get_with_retry, post_with_retry


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

def test_authenticated_get():
    with patch('src.utils.middleware.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "secure"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = authenticated_get("https://api.example.com/secure", "token123")
        assert result["data"] == "secure"


# --- Async retry tests ---

def test_retry_request_success():
    async def success_func():
        return "ok"
    result = asyncio.run(retry_request(success_func))
    assert result == "ok"


def test_retry_request_retries_on_failure():
    call_count = 0

    async def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise httpx.HTTPError("fail")
        return "recovered"

    result = asyncio.run(retry_request(flaky_func, max_retries=3, backoff=0.01))
    assert result == "recovered"
    assert call_count == 3


def test_retry_request_exhausts_retries():
    async def always_fail():
        raise httpx.HTTPError("permanent failure")

    with pytest.raises(httpx.HTTPError):
        asyncio.run(retry_request(always_fail, max_retries=2, backoff=0.01))


def test_get_with_retry():
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "data"}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch('src.utils.retry.httpx.AsyncClient', return_value=mock_client):
        result = asyncio.run(get_with_retry("https://api.example.com/test"))
        assert result == {"result": "data"}


def test_post_with_retry():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "456"}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch('src.utils.retry.httpx.AsyncClient', return_value=mock_client):
        result = asyncio.run(post_with_retry("https://api.example.com/test", data={"key": "val"}))
        assert result == {"id": "456"}
