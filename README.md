# EVE Healthcare API

Backend service for booking diagnostic tests at centres, with JWT authentication, simulated payments, and an idempotent payment webhook.

## Tech Stack

FastAPI · PostgreSQL · SQLAlchemy · JWT · Docker · Pytest

## Features

- Signup/login with JWT authentication
- Diagnostic centres and tests, with centre-specific pricing
- Authenticated bookings (users see only their own)
- Simulated payments and payment webhooks
- Idempotent webhook handling via a unique `event_id`
- Input validation and consistent error responses
- Automated tests

## Getting Started

### Option 1: Docker (recommended)

```bash
docker compose up --build
```

### Option 2: Local

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/eve_healthcare
SECRET_KEY=your-secret-key
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Interactive docs: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint             | Auth | Purpose                  |
|--------|----------------------|------|--------------------------|
| POST   | `/auth/signup`       | No   | Register a user          |
| POST   | `/auth/login`        | No   | Get a JWT token          |
| GET    | `/centres/`          | No   | List centres             |
| GET    | `/tests/`            | No   | List tests               |
| POST   | `/bookings/`         | Yes  | Create a booking         |
| GET    | `/bookings/`         | Yes  | List your bookings       |
| POST   | `/payments/`         | Yes  | Simulate a payment       |
| POST   | `/payments/webhook/` | No   | Receive payment events   |

## Payment Flow

1. User creates a booking, which starts as `PENDING`.
2. User pays via `POST /payments/`.
3. Successful payment moves the booking to `CONFIRMED`; failed payment moves it to `FAILED`.
4. The webhook can also update payment status. Each event carries a unique `event_id`, so a repeated delivery is ignored instead of being processed twice.

## Design Decisions

- **Idempotency:** `event_id` is stored with a unique constraint, so duplicate webhooks cannot double-confirm a booking.
- **Amount check:** the webhook amount must match the booking amount, otherwise the event is rejected.
- **Centre-specific pricing:** price lives on the centre-test relationship, not on the test itself.

## Testing

```bash
pytest
```

## Assumptions

- Payments are simulated; no real gateway is integrated.
- Centre/test management is not admin-restricted yet.
- PostgreSQL is the only supported database.

## Future Improvements

- Alembic migrations
- Admin roles for centre/test management
- Real payment gateway integration
- Webhook signature verification
- Redis/Celery for background processing
- Rate limiting