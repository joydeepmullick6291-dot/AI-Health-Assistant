from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentResponse)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointment = Appointment(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        appointment_date=payload.appointment_date,
        appointment_time=payload.appointment_time,
        reason=payload.reason,
        status="pending",
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.get("/", response_model=list[AppointmentResponse])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)
    return appointment

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}