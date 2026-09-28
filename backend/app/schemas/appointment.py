from pydantic import BaseModel, ConfigDict
from datetime import date, time
from typing import Literal, Optional

AppointmentStatus = Literal["pending", "confirmed", "completed", "cancelled"]


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[AppointmentStatus] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus
    reason: Optional[str] = None
    notes: Optional[str] = None