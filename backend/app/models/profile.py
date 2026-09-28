from sqlalchemy import Column, BigInteger, ForeignKey, String, Text, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(BigInteger, ForeignKey("patients.id"), nullable=False, unique=True)

    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    blood_group = Column(String(10), nullable=True)

    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)

    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)

    allergies = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", backref="profile")