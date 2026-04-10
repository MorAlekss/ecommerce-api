# ecommerce-api

E-commerce API client library — uses `requests` for HTTP calls.

**⚠️ Migration target:** This codebase is to be migrated from `requests` (sync) to `httpx` async.

## Structure

```
src/
├── auth/          # Authentication: login, OAuth, API tokens
├── users/         # User management: profile, admin, preferences
├── products/      # Product catalog, search, inventory
├── orders/        # Checkout, order history, returns
├── payments/      # Stripe payments, webhooks
├── notifications/ # Email and SMS notifications
└── utils/         # HTTP utilities, retry logic, middleware
tests/
├── unit/          # Unit tests per module
└── integration/   # Integration tests
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

## Running tests

```bash
python -m pytest tests/ -v
```
