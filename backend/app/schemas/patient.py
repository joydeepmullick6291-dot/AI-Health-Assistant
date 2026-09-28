from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientCreate(BaseModel):
    user_id: int
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

class PatientResponse(BaseModel):
    id: int
    user_id: int
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

    class Config:
        from_attributes = True