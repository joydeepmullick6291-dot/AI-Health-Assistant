from sqlalchemy import Column, BigInteger, ForeignKey, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class LabReport(Base):
    __tablename__ = "lab_reports"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    appointment_id = Column(BigInteger, ForeignKey("appointments.id"), nullable=True)

    test_name = Column(String(150), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    result_summary = Column(Text, nullable=True)
    result_details = Column(Text, nullable=True)
    report_file_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", backref="lab_reports")
    doctor = relationship("Doctor", backref="lab_reports")
    appointment = relationship("Appointment", backref="lab_reports")