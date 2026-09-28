from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    gender = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    blood_group = Column(String(10), nullable=True)
    address = Column(String(255), nullable=True)
    emergency_contact = Column(String(20), nullable=True)

    user = relationship("User", backref="patient_profile")