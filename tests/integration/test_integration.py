import sys
sys.path.insert(0, '.')
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

# Pre-import all modules so patches target the module-level httpx reference
import src.auth.login
import src.products.catalog
import src.orders.checkout
import src.payments.stripe


def make_mock_response(data):
    m = MagicMock()
    m.json.return_value = data
    m.raise_for_status = MagicMock(return_value=None)
    m.status_code = 200
    return m


def make_async_return(value):
    """Create a coroutine function that returns the given value (for mocking async calls)."""
    async def _coro(*args, **kwargs):
        return value
    return _coro


@pytest.mark.asyncio
async def test_full_purchase_flow():
    """Integration test: login → get product → add to cart → checkout → payment"""
    login_resp = make_mock_response({"access_token": "tok123"})
    product_resp = make_mock_response({"id": "p1", "name": "Widget", "price": 999})
    cart_resp = make_mock_response({"id": "cart1", "total": 999})
    payment_resp = make_mock_response({"id": "pi_123", "status": "requires_confirmation"})

    # Create separate mock clients — each module's __aenter__ must yield a unique client
    mock_client_login = AsyncMock()
    mock_client_login.post = make_async_return(login_resp)

    mock_client_catalog = AsyncMock()
    mock_client_catalog.get = make_async_return(product_resp)

    mock_client_checkout = AsyncMock()
    mock_client_checkout.post = make_async_return(cart_resp)

    mock_client_stripe = AsyncMock()
    mock_client_stripe.post = make_async_return(payment_resp)

    # All modules share the same httpx module object, so patching httpx.AsyncClient
    # on one module patches it for all. We use a class whose __new__ returns a
    # context manager yielding the correct client based on call order.
    call_count = [0]
    clients = [mock_client_login, mock_client_catalog, mock_client_checkout, mock_client_stripe]

    def make_ctx_for_client(client):
        ctx = AsyncMock()
        ctx.__aenter__.return_value = client
        ctx.__aexit__.return_value = False
        return ctx

    class MockAsyncClient:
        def __new__(cls, *args, **kwargs):
            idx = call_count[0]
            call_count[0] += 1
            return make_ctx_for_client(clients[idx])

    with patch('src.auth.login.httpx.AsyncClient', MockAsyncClient), \
         patch('src.products.catalog.httpx.AsyncClient', MockAsyncClient), \
         patch('src.orders.checkout.httpx.AsyncClient', MockAsyncClient), \
         patch('src.payments.stripe.httpx.AsyncClient', MockAsyncClient):

        from src.auth.login import login
        from src.products.catalog import get_product
        from src.orders.checkout import create_cart
        from src.payments.stripe import create_payment_intent

        auth = await login("user@example.com", "password")
        token = auth["access_token"]
        assert token == "tok123"

        product = await get_product("p1")
        assert product["name"] == "Widget"

        cart = await create_cart(token)
        assert cart["id"] == "cart1"

        payment = await create_payment_intent(product["price"], "usd")
        assert payment["id"] == "pi_123"
