import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import MagicMock, AsyncMock
import types

# Create a mock httpx module with AsyncClient that works as context manager
_httpx_mock = types.ModuleType('httpx')
_mock_async_client_cls = MagicMock()
_httpx_mock.AsyncClient = _mock_async_client_cls

# Pre-inject into sys.modules so source modules can import it
sys.modules['httpx'] = _httpx_mock

from src.users.profile import get_profile, update_profile  # noqa: E402
from src.users.admin import list_users  # noqa: E402
from src.users.preferences import get_preferences  # noqa: E402


@pytest.mark.asyncio
async def test_get_profile():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "u1", "name": "Alice", "email": "alice@example.com"}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    _mock_async_client_cls.return_value.__aenter__.return_value = mock_client
    _mock_async_client_cls.return_value.__aexit__.return_value = False

    result = await get_profile("u1", "token123")
    assert result["name"] == "Alice"


@pytest.mark.asyncio
async def test_update_profile():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "u1", "name": "Alice Updated"}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.put.return_value = mock_response

    _mock_async_client_cls.return_value.__aenter__.return_value = mock_client
    _mock_async_client_cls.return_value.__aexit__.return_value = False

    result = await update_profile("u1", "token123", {"name": "Alice Updated"})
    assert result["name"] == "Alice Updated"


@pytest.mark.asyncio
async def test_list_users():
    mock_response = MagicMock()
    mock_response.json.return_value = {"users": [{"id": "u1"}, {"id": "u2"}], "total": 2}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    _mock_async_client_cls.return_value.__aenter__.return_value = mock_client
    _mock_async_client_cls.return_value.__aexit__.return_value = False

    result = await list_users("admin_token")
    assert result["total"] == 2


@pytest.mark.asyncio
async def test_get_preferences():
    mock_response = MagicMock()
    mock_response.json.return_value = {"theme": "dark", "language": "en"}
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    _mock_async_client_cls.return_value.__aenter__.return_value = mock_client
    _mock_async_client_cls.return_value.__aexit__.return_value = False

    result = await get_preferences("u1", "token123")
    assert result["theme"] == "dark"
