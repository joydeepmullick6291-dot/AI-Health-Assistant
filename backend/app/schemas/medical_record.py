from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: int
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_id: Optional[int] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_id: int
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True