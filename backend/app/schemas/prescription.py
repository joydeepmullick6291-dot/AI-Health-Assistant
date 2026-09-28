from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    medical_record_id: Optional[int] = None
    medication_name: str
    dosage: str
    frequency: str
    duration: str
    instructions: Optional[str] = None


class PrescriptionUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_id: Optional[int] = None
    medical_record_id: Optional[int] = None
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None


class PrescriptionResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    medical_record_id: Optional[int] = None
    medication_name: str
    dosage: str
    frequency: str
    duration: str
    instructions: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True