from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ProfileCreate(BaseModel):
    patient_id: int
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None


class ProfileUpdate(BaseModel):
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    patient_id: int
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True