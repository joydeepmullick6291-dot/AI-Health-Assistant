from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.profile import Profile
from app.models.patient import Patient
from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("/", response_model=ProfileResponse)
def create_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_profile = db.query(Profile).filter(Profile.patient_id == payload.patient_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists for this patient")

    profile = Profile(**payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/", response_model=list[ProfileResponse])
def list_profiles(db: Session = Depends(get_db)):
    return db.query(Profile).all()


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.get("/patient/{patient_id}", response_model=ProfileResponse)
def get_profile_by_patient(patient_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.patient_id == patient_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found for this patient")

    return profile


@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(profile_id: int, payload: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


@router.delete("/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(profile)
    db.commit()
    return {"message": "Profile deleted successfully"}