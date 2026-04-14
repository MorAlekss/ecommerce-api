import sys
sys.path.insert(0, '.')
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from src.utils.http import get, post, put, patch as http_patch, delete
from src.utils.middleware import authenticated_get, authenticated_post
import httpx
from src.utils.retry import get_with_retry, post_with_retry, retry_request


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


def test_get_with_retry():
    async def _run():
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "value"}
        mock_response.raise_for_status.return_value = None
        mock_client.get.return_value = mock_response
        with patch('src.utils.retry.httpx.AsyncClient') as mock_ac:
            mock_ac.return_value.__aenter__.return_value = mock_client
            result = await get_with_retry("https://api.example.com/test")
            assert result["data"] == "value"
    asyncio.run(_run())


def test_post_with_retry():
    async def _run():
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "456"}
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value = mock_response
        with patch('src.utils.retry.httpx.AsyncClient') as mock_ac:
            mock_ac.return_value.__aenter__.return_value = mock_client
            result = await post_with_retry("https://api.example.com/test", data={"key": "value"})
            assert result["id"] == "456"
    asyncio.run(_run())


def test_retry_request_retries_on_failure():
    async def _run():
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "recovered"}
        mock_response.raise_for_status.return_value = None
        call_count = 0

        async def failing_then_success(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise httpx.RequestError("connection failed")
            return mock_response

        mock_client.get = failing_then_success
        with patch('src.utils.retry.httpx.AsyncClient') as mock_ac:
            mock_ac.return_value.__aenter__.return_value = mock_client
            result = await get_with_retry("https://api.example.com/test", max_retries=3)
            assert result["data"] == "recovered"
            assert call_count == 3
    asyncio.run(_run())
