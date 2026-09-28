from sqlalchemy import Column, BigInteger, ForeignKey, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    appointment_id = Column(BigInteger, ForeignKey("appointments.id"), nullable=True)
    medical_record_id = Column(BigInteger, ForeignKey("medical_records.id"), nullable=True)

    medication_name = Column(String(150), nullable=False)
    dosage = Column(String(100), nullable=False)
    frequency = Column(String(100), nullable=False)
    duration = Column(String(100), nullable=False)
    instructions = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", backref="prescriptions")
    doctor = relationship("Doctor", backref="prescriptions")
    appointment = relationship("Appointment", backref="prescriptions")
    medical_record = relationship("MedicalRecord", backref="prescriptions")