from sqlalchemy import Column, BigInteger, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id"), nullable=False)
    appointment_id = Column(BigInteger, ForeignKey("appointments.id"), nullable=False)

    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    prescription = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", backref="medical_records")
    doctor = relationship("Doctor", backref="medical_records")
    appointment = relationship("Appointment", backref="medical_records")