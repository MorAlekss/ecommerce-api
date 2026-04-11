import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.users.profile import get_profile, update_profile, update_avatar, delete_account
from src.users.admin import list_users, get_user, suspend_user
from src.users.preferences import get_preferences, update_preferences


@pytest.mark.asyncio
async def test_get_profile():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "u1", "name": "Alice", "email": "alice@example.com"}
    mock_response.raise_for_status.return_value = None
    with patch('src.users.profile.httpx.AsyncClient') as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client
        result = await get_profile("u1", "token123")
        assert result["name"] == "Alice"

@pytest.mark.asyncio
async def test_update_profile():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "u1", "name": "Alice Updated"}
    mock_response.raise_for_status.return_value = None
    with patch('src.users.profile.httpx.AsyncClient') as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.put.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client
        result = await update_profile("u1", "token123", {"name": "Alice Updated"})
        assert result["name"] == "Alice Updated"

def test_list_users():
    with patch('src.users.admin.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"users": [{"id": "u1"}, {"id": "u2"}], "total": 2}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = list_users("admin_token")
        assert result["total"] == 2

def test_get_preferences():
    with patch('src.users.preferences.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"theme": "dark", "language": "en"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = get_preferences("u1", "token123")
        assert result["theme"] == "dark"
