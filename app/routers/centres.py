from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CentreTest, DiagnosticCentre, Test
from app.schemas import (
    CentreCreate,
    CentreResponse,
    CentreTestCreate,
    CentreTestResponse,
    TestCreate,
    TestResponse,
)

router = APIRouter(
    prefix="/centres",
    tags=["Diagnostic Centres"]
)


@router.get("/", response_model=list[CentreResponse])
def get_centres(
    db: Session = Depends(get_db)
):
    return db.query(DiagnosticCentre).all()


@router.get("/{centre_id}", response_model=CentreResponse)
def get_centre(
    centre_id: int,
    db: Session = Depends(get_db)
):
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

    return centre


@router.post(
    "/",
    response_model=CentreResponse,
    status_code=status.HTTP_201_CREATED
)
def create_centre(
    centre_data: CentreCreate,
    db: Session = Depends(get_db)
):
    centre = DiagnosticCentre(
        name=centre_data.name,
        location=centre_data.location
    )

    db.add(centre)
    db.commit()
    db.refresh(centre)

    return centre


@router.post(
    "/{centre_id}/tests",
    response_model=CentreTestResponse,
    status_code=status.HTTP_201_CREATED
)
def add_test_to_centre(
    centre_id: int,
    test_data: CentreTestCreate,
    db: Session = Depends(get_db)
):
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
        .filter(Test.id == test_data.test_id)
        .first()
    )

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic test not found"
        )

    existing = (
        db.query(CentreTest)
        .filter(
            CentreTest.centre_id == centre_id,
            CentreTest.test_id == test_data.test_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Test is already available at this centre"
        )

    centre_test = CentreTest(
        centre_id=centre_id,
        test_id=test_data.test_id,
        price=test_data.price
    )

    db.add(centre_test)
    db.commit()
    db.refresh(centre_test)

    return centre_test


@router.get(
    "/{centre_id}/tests",
    response_model=list[CentreTestResponse]
)
def get_centre_tests(
    centre_id: int,
    db: Session = Depends(get_db)
):
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

    return (
        db.query(CentreTest)
        .filter(CentreTest.centre_id == centre_id)
        .all()
    )


# Test management

test_router = APIRouter(
    prefix="/tests",
    tags=["Diagnostic Tests"]
)


@test_router.get("/", response_model=list[TestResponse])
def get_tests(
    db: Session = Depends(get_db)
):
    return db.query(Test).all()


@test_router.get("/{test_id}", response_model=TestResponse)
def get_test(
    test_id: int,
    db: Session = Depends(get_db)
):
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

    return test


@test_router.post(
    "/",
    response_model=TestResponse,
    status_code=status.HTTP_201_CREATED
)
def create_test(
    test_data: TestCreate,
    db: Session = Depends(get_db)
):
    test = Test(
        name=test_data.name,
        description=test_data.description
    )

    db.add(test)
    db.commit()
    db.refresh(test)

    return test