from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorResponse

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.post("/", response_model=DoctorResponse)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(Doctor).filter(Doctor.user_id == payload.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Doctor profile already exists")

    doctor = Doctor(**payload.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

@router.get("/", response_model=list[DoctorResponse])
def list_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor