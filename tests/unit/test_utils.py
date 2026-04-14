import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.utils.http import get, post, put, patch as http_patch, delete


@pytest.mark.asyncio
async def test_get():
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "value"}
    mock_response.raise_for_status.return_value = None
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    with patch('src.utils.http.httpx.AsyncClient') as mock_cls:
        mock_cls.return_value.__aenter__.return_value = mock_client
        result = await get("https://api.example.com/test")
        assert result["data"] == "value"

@pytest.mark.asyncio
async def test_post():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "123"}
    mock_response.raise_for_status.return_value = None
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    with patch('src.utils.http.httpx.AsyncClient') as mock_cls:
        mock_cls.return_value.__aenter__.return_value = mock_client
        result = await post("https://api.example.com/test", {"key": "value"})
        assert result["id"] == "123"

@pytest.mark.asyncio
async def test_put():
    mock_response = MagicMock()
    mock_response.json.return_value = {"updated": True}
    mock_response.raise_for_status.return_value = None
    mock_client = AsyncMock()
    mock_client.put.return_value = mock_response
    with patch('src.utils.http.httpx.AsyncClient') as mock_cls:
        mock_cls.return_value.__aenter__.return_value = mock_client
        result = await put("https://api.example.com/test", {"key": "value"})
        assert result["updated"] is True

@pytest.mark.asyncio
async def test_http_patch():
    mock_response = MagicMock()
    mock_response.json.return_value = {"patched": True}
    mock_response.raise_for_status.return_value = None
    mock_client = AsyncMock()
    mock_client.patch.return_value = mock_response
    with patch('src.utils.http.httpx.AsyncClient') as mock_cls:
        mock_cls.return_value.__aenter__.return_value = mock_client
        result = await http_patch("https://api.example.com/test", {"key": "value"})
        assert result["patched"] is True

@pytest.mark.asyncio
async def test_delete():
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.raise_for_status.return_value = None
    mock_client = AsyncMock()
    mock_client.delete.return_value = mock_response
    with patch('src.utils.http.httpx.AsyncClient') as mock_cls:
        mock_cls.return_value.__aenter__.return_value = mock_client
        result = await delete("https://api.example.com/test")
        assert result == 204
