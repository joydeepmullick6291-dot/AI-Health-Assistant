from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.lab_report import LabReport
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.schemas.lab_report import (
    LabReportCreate,
    LabReportUpdate,
    LabReportResponse,
)

router = APIRouter(prefix="/lab-reports", tags=["lab-reports"])


@router.post("/", response_model=LabReportResponse)
def create_lab_report(payload: LabReportCreate, db: Session = Depends(get_db)):
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

    lab_report = LabReport(**payload.model_dump())
    db.add(lab_report)
    db.commit()
    db.refresh(lab_report)
    return lab_report


@router.get("/", response_model=list[LabReportResponse])
def list_lab_reports(db: Session = Depends(get_db)):
    return db.query(LabReport).all()


@router.get("/{lab_report_id}", response_model=LabReportResponse)
def get_lab_report(lab_report_id: int, db: Session = Depends(get_db)):
    lab_report = db.query(LabReport).filter(LabReport.id == lab_report_id).first()

    if not lab_report:
        raise HTTPException(status_code=404, detail="Lab report not found")

    return lab_report


@router.put("/{lab_report_id}", response_model=LabReportResponse)
def update_lab_report(
    lab_report_id: int,
    payload: LabReportUpdate,
    db: Session = Depends(get_db)
):
    lab_report = db.query(LabReport).filter(LabReport.id == lab_report_id).first()

    if not lab_report:
        raise HTTPException(status_code=404, detail="Lab report not found")

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

    for key, value in update_data.items():
        setattr(lab_report, key, value)

    db.commit()
    db.refresh(lab_report)
    return lab_report


@router.delete("/{lab_report_id}")
def delete_lab_report(lab_report_id: int, db: Session = Depends(get_db)):
    lab_report = db.query(LabReport).filter(LabReport.id == lab_report_id).first()

    if not lab_report:
        raise HTTPException(status_code=404, detail="Lab report not found")

    db.delete(lab_report)
    db.commit()
    return {"message": "Lab report deleted successfully"}