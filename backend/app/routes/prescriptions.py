from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.prescription import Prescription
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse,
)

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])


@router.post("/", response_model=PrescriptionResponse)
def create_prescription(payload: PrescriptionCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if payload.appointment_id is not None:
        appointment = db.query(Appointment).filter(Appointment.id == payload.appointment_id).first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

    if payload.medical_record_id is not None:
        medical_record = db.query(MedicalRecord).filter(MedicalRecord.id == payload.medical_record_id).first()
        if not medical_record:
            raise HTTPException(status_code=404, detail="Medical record not found")

    prescription = Prescription(**payload.model_dump())
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription


@router.get("/", response_model=list[PrescriptionResponse])
def list_prescriptions(db: Session = Depends(get_db)):
    return db.query(Prescription).all()


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()

    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    return prescription


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: int,
    payload: PrescriptionUpdate,
    db: Session = Depends(get_db)
):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()

    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "patient_id" in update_data:
        patient = db.query(Patient).filter(Patient.id == update_data["patient_id"]).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

    if "doctor_id" in update_data:
        doctor = db.query(Doctor).filter(Doctor.id == update_data["doctor_id"]).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

    if "appointment_id" in update_data and update_data["appointment_id"] is not None:
        appointment = db.query(Appointment).filter(Appointment.id == update_data["appointment_id"]).first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

    if "medical_record_id" in update_data and update_data["medical_record_id"] is not None:
        medical_record = db.query(MedicalRecord).filter(MedicalRecord.id == update_data["medical_record_id"]).first()
        if not medical_record:
            raise HTTPException(status_code=404, detail="Medical record not found")

    for key, value in update_data.items():
        setattr(prescription, key, value)

    db.commit()
    db.refresh(prescription)
    return prescription


@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()

    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    db.delete(prescription)
    db.commit()
    return {"message": "Prescription deleted successfully"}