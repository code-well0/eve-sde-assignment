from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# Authentication

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

# Diagnostic Centres

class CentreCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    location: str = Field(min_length=2, max_length=255)


class CentreResponse(BaseModel):
    id: int
    name: str
    location: str

    model_config = ConfigDict(from_attributes=True)

# Tests

class TestCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)


class TestResponse(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)


class CentreTestCreate(BaseModel):
    test_id: int
    price: Decimal = Field(gt=0)


class CentreTestResponse(BaseModel):
    id: int
    centre_id: int
    test_id: int
    price: Decimal

    model_config = ConfigDict(from_attributes=True)

# Bookings

class BookingCreate(BaseModel):
    centre_id: int
    test_id: int
    appointment_at: datetime


class BookingResponse(BaseModel):
    id: int
    user_id: int
    centre_id: int
    test_id: int
    appointment_at: datetime
    amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Payments

class PaymentRequest(BaseModel):
    booking_id: int


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: Decimal
    status: str
    provider_event_id: str

    model_config = ConfigDict(from_attributes=True)


class PaymentWebhook(BaseModel):
    event_id: str = Field(min_length=1, max_length=100)
    booking_id: int
    status: str
    amount: Decimal = Field(gt=0)