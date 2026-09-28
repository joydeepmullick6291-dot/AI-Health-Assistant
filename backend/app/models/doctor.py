from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    specialization = Column(String(100), nullable=False)
    license_number = Column(String(100), unique=True, nullable=False)
    department = Column(String(100), nullable=True)
    experience_years = Column(Integer, nullable=True)

    user = relationship("User", backref="doctor_profile")