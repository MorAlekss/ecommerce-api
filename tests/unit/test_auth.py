import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import patch, MagicMock
from src.auth.login import login, logout, refresh_token, verify_email
from src.auth.oauth import get_oauth_url, exchange_oauth_code
from src.auth.tokens import get_api_tokens, create_api_token, revoke_api_token


def test_login():
    with patch('src.auth.login.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "token123", "refresh_token": "refresh123"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = login("user@example.com", "password")
        assert result["access_token"] == "token123"

def test_logout():
    with patch('src.auth.login.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = logout("token123")
        assert result == 200

def test_refresh_token():
    with patch('src.auth.login.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "new_token"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = refresh_token("refresh123")
        assert result["access_token"] == "new_token"

def test_get_oauth_url():
    with patch('src.auth.oauth.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"url": "https://oauth.example.com/auth"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = get_oauth_url("google", "https://app.example.com/callback")
        assert "url" in result

def test_create_api_token():
    with patch('src.auth.tokens.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "tok_123", "name": "My Token"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        result = create_api_token("user1", "token123", "My Token", ["read"])
        assert result["id"] == "tok_123"
