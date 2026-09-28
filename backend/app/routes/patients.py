from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientResponse)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(Patient).filter(Patient.user_id == payload.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient profile already exists")

    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("/", response_model=list[PatientResponse])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient