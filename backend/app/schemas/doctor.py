from pydantic import BaseModel
from typing import Optional

class DoctorCreate(BaseModel):
    user_id: int
    specialization: str
    license_number: str
    department: Optional[str] = None
    experience_years: Optional[int] = None

class DoctorResponse(BaseModel):
    id: int
    user_id: int
    specialization: str
    license_number: str
    department: Optional[str] = None
    experience_years: Optional[int] = None

    class Config:
        from_attributes = True