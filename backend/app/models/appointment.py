from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(String(20), default="pending")
    reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    patient = relationship("Patient", backref="appointments")
    doctor = relationship("Doctor", backref="appointments")