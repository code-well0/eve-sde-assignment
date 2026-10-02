# EVE Healthcare API

A backend service for booking diagnostic tests at partner centres. It handles user authentication, centre-specific test pricing, bookings, simulated payments, and an idempotent payment webhook.

**Repository:** https://github.com/code-well0/eve-sde-assignment

---

## Tech Stack

| Layer          | Choice                  |
| -------------- | ----------------------- |
| Framework      | FastAPI                 |
| Database       | PostgreSQL + SQLAlchemy |
| Auth           | JWT (bearer tokens)     |
| Testing        | Pytest                  |
| Infrastructure | Docker, Docker Compose  |

## Features

- Signup and login with JWT authentication
- Diagnostic centres and tests, with **centre-specific pricing**
- Authenticated bookings; users can only see their own
- Cancellation of eligible bookings
- Simulated payments with webhook support
- **Idempotent webhook handling** using a unique `event_id`
- Input validation and consistent error responses
- Automated test suite
- One-command Docker setup (API + PostgreSQL)

---

## Getting Started

### Option 1: Docker (recommended)

```bash
docker compose up --build
```

The API runs at `http://localhost:8000`.

### Option 2: Local setup

**1. Create a virtual environment and install dependencies**

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

**2. Configure environment variables**

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/eve_healthcare
SECRET_KEY=your-secret-key
```

Make sure PostgreSQL is running and the `eve_healthcare` database exists.

**3. Start the server**

```bash
uvicorn app.main:app --reload
```

### Useful URLs

| URL                            | Description                      |
| ------------------------------ | -------------------------------- |
| http://localhost:8000/docs     | Interactive Swagger documentation |
| http://localhost:8000/health   | Health check                     |

---

## API Reference

Request and response schemas are available in the interactive docs at `/docs`.

| Method | Endpoint                        | Auth | Description               |
| ------ | ------------------------------- | :--: | ------------------------- |
| POST   | `/auth/signup`                  |  No  | Register a new user       |
| POST   | `/auth/login`                   |  No  | Log in and receive a JWT  |
| GET    | `/centres/`                     |  No  | List diagnostic centres   |
| GET    | `/centres/{centre_id}`          |  No  | Get a single centre       |
| GET    | `/tests/`                       |  No  | List diagnostic tests     |
| GET    | `/tests/{test_id}`              |  No  | Get a single test         |
| POST   | `/bookings/`                    | Yes  | Create a booking          |
| GET    | `/bookings/`                    | Yes  | List your bookings        |
| GET    | `/bookings/{booking_id}`        | Yes  | Get one of your bookings  |
| PATCH  | `/bookings/{booking_id}/cancel` | Yes  | Cancel a booking          |
| POST   | `/payments/`                    | Yes  | Make a simulated payment  |
| POST   | `/payments/webhook/`            |  No  | Receive payment events    |
| GET    | `/health`                       |  No  | Service health check      |

Protected endpoints expect the header `Authorization: Bearer <token>`.

---

## How Payments Work

```
Booking created ──► PENDING ──┬─► payment succeeds ──► CONFIRMED
                              └─► payment fails    ──► FAILED
```

1. A new booking starts as `PENDING`.
2. The user pays through `POST /payments/`.
3. A successful payment confirms the booking; a failed one marks it `FAILED`.
4. A payment provider can also report the outcome through the webhook.
5. Every webhook event carries a unique `event_id`. If the same event arrives twice, the existing payment record is returned and nothing is processed again.

---

## Design Decisions

- **Idempotent webhooks:** `event_id` has a unique database constraint, so retried deliveries can never create duplicate payments or double-confirm a booking.
- **Amount validation:** a webhook is rejected if its amount does not match the booking amount.
- **Centre-specific pricing:** price is stored on the centre-test relationship, because the same test can cost different amounts at different centres.
- **Ownership checks:** every booking query is scoped to the authenticated user.
- **Separated business logic:** booking, payment, and webhook rules live outside the route handlers, which keeps routes thin and logic testable.

---

## Testing

```bash
pytest
```

The suite covers authentication, input validation, protected endpoints, bookings, payments, and webhook validation.

---

## Assumptions

- Payments are simulated; no real payment gateway is integrated.
- Centre and test management endpoints are not admin-restricted in this version.
- PostgreSQL is the supported database.
- Appointment times must be in the future.
- The booking amount comes from the price configured for the selected centre and test.
- `event_id` uniquely identifies a payment webhook event.

---

## Future Improvements

- Alembic database migrations
- Admin roles for centre and test management
- Real payment gateway integration
- Webhook signature verification
- Background processing with Redis/Celery
- Rate limiting
- Pagination on list endpoints
- Structured logging