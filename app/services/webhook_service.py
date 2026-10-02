from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Booking, Payment


def process_webhook(
    db: Session,
    event_id: str,
    booking_id: int,
    payment_status: str,
    amount
):
    # Check if this event was already processed
    existing_payment = db.query(Payment).filter(
        Payment.provider_event_id == event_id
    ).first()

    if existing_payment:
        return existing_payment

    # Find booking
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Make sure webhook amount matches booking amount
    if amount != booking.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount does not match booking amount"
        )

    # Validate payment status
    if payment_status not in ["SUCCESS", "FAILED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment status"
        )

    payment = Payment(
        booking_id=booking.id,
        provider_event_id=event_id,
        amount=amount,
        status=payment_status
    )

    if payment_status == "SUCCESS":
        booking.status = "CONFIRMED"
    else:
        booking.status = "FAILED"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment