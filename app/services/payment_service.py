import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import Booking, Payment


def process_payment(
    db: Session,
    booking: Booking
):
    if booking.status == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot pay for a cancelled booking"
        )

    if booking.status == "CONFIRMED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already paid"
        )

    payment_success = True

    payment_status = "SUCCESS" if payment_success else "FAILED"

    payment = Payment(
        booking_id=booking.id,
        provider_event_id=str(uuid.uuid4()),
        amount=booking.amount,
        status=payment_status
    )

    booking.status = (
        "CONFIRMED" if payment_success else "FAILED"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment