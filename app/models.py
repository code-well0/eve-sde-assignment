from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user")


class DiagnosticCentre(Base):
    __tablename__ = "diagnostic_centres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    location = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tests = relationship("CentreTest", back_populates="centre")
    bookings = relationship("Booking", back_populates="centre")


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)

    centres = relationship("CentreTest", back_populates="test")
    bookings = relationship("Booking", back_populates="test")


class CentreTest(Base):
    __tablename__ = "centre_tests"

    id = Column(Integer, primary_key=True, index=True)
    centre_id = Column(
        Integer,
        ForeignKey("diagnostic_centres.id"),
        nullable=False
    )
    test_id = Column(
        Integer,
        ForeignKey("tests.id"),
        nullable=False
    )
    price = Column(Numeric(10, 2), nullable=False)

    centre = relationship("DiagnosticCentre", back_populates="tests")
    test = relationship("Test", back_populates="centres")

    __table_args__ = (
        UniqueConstraint(
            "centre_id",
            "test_id",
            name="unique_centre_test"
        ),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    centre_id = Column(
        Integer,
        ForeignKey("diagnostic_centres.id"),
        nullable=False
    )

    test_id = Column(
        Integer,
        ForeignKey("tests.id"),
        nullable=False
    )

    appointment_at = Column(DateTime, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    status = Column(
        String(20),
        default="PENDING",
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    centre = relationship("DiagnosticCentre", back_populates="bookings")
    test = relationship("Test", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False
    )

    provider_event_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    amount = Column(Numeric(10, 2), nullable=False)

    status = Column(
        String(20),
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Booking", back_populates="payments")