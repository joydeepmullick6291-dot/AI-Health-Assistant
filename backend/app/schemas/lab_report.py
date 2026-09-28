from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LabReportCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    test_name: str
    status: str = "pending"
    result_summary: Optional[str] = None
    result_details: Optional[str] = None
    report_file_url: Optional[str] = None


class LabReportUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_id: Optional[int] = None
    test_name: Optional[str] = None
    status: Optional[str] = None
    result_summary: Optional[str] = None
    result_details: Optional[str] = None
    report_file_url: Optional[str] = None


class LabReportResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    test_name: str
    status: str
    result_summary: Optional[str] = None
    result_details: Optional[str] = None
    report_file_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True