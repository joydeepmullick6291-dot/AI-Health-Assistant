from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse,
)

router = APIRouter(prefix="/medical-records", tags=["medical-records"])


@router.post("/", response_model=MedicalRecordResponse)
def create_medical_record(payload: MedicalRecordCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id).first()
    appointment = db.query(Appointment).filter(Appointment.id == payload.appointment_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    record = MedicalRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[MedicalRecordResponse])
def list_medical_records(db: Session = Depends(get_db)):
    return db.query(MedicalRecord).all()


@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")

    return record


@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: int,
    payload: MedicalRecordUpdate,
    db: Session = Depends(get_db)
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "patient_id" in update_data:
        patient = db.query(Patient).filter(Patient.id == update_data["patient_id"]).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

    if "doctor_id" in update_data:
        doctor = db.query(Doctor).filter(Doctor.id == update_data["doctor_id"]).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

    if "appointment_id" in update_data:
        appointment = db.query(Appointment).filter(Appointment.id == update_data["appointment_id"]).first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}")
def delete_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")

    db.delete(record)
    db.commit()
    return {"message": "Medical record deleted successfully"}