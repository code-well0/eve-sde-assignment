from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import Booking, CentreTest, DiagnosticCentre, Test, User

def create_booking(
    db: Session,
    user: User,
    centre_id: int,
    test_id: int,
    appointment_at: datetime
):
    if appointment_at <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment time must be in the future"
        )

    centre = (
        db.query(DiagnosticCentre)
        .filter(DiagnosticCentre.id == centre_id)
        .first()
    )

    if not centre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic centre not found"
        )

    test = (
        db.query(Test)
        .filter(Test.id == test_id)
        .first()
    )

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic test not found"
        )

    centre_test = (
        db.query(CentreTest)
        .filter(
            CentreTest.centre_id == centre_id,
            CentreTest.test_id == test_id
        )
        .first()
    )

    if not centre_test:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This test is not available at the selected centre"
        )

    booking = Booking(
        user_id=user.id,
        centre_id=centre_id,
        test_id=test_id,
        appointment_at=appointment_at,
        amount=centre_test.price,
        status="PENDING"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking