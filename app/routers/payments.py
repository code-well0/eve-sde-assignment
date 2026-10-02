from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Booking, User
from app.schemas import PaymentRequest, PaymentResponse, PaymentWebhook
from app.services.payment_service import process_payment
from app.services.webhook_service import process_webhook

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def make_payment(
    payment_data: PaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == payment_data.booking_id,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    return process_payment(
        db=db,
        booking=booking
    )

@router.post("/webhook/", response_model=PaymentResponse)
def payment_webhook(
    webhook_data: PaymentWebhook,
    db: Session = Depends(get_db)
):
    return process_webhook(
        db=db,
        event_id=webhook_data.event_id,
        booking_id=webhook_data.booking_id,
        payment_status=webhook_data.status,
        amount=webhook_data.amount
    )