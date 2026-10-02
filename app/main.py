from fastapi import FastAPI
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.centres import router as centre_router
from app.routers.centres import test_router
from app.routers.bookings import router as booking_router
from app.routers.payments import router as payment_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="EVE Healthcare API",
    description="Backend service for diagnostic test bookings and simulated payments.",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(centre_router)
app.include_router(test_router)
app.include_router(booking_router)
app.include_router(payment_router)


@app.get("/")
def root():
    return {
        "message": "EVE Healthcare API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }