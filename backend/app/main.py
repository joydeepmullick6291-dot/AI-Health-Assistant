from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription
from app.models.lab_report import LabReport
from app.models.profile import Profile

from app.routes.auth import router as auth_router
from app.routes.doctors import router as doctors_router
from app.routes.patients import router as patients_router
from app.routes.appointments import router as appointments_router
from app.routes.medical_records import router as medical_records_router
from app.routes.prescriptions import router as prescriptions_router
from app.routes.lab_reports import router as lab_reports_router
from app.routes.profiles import router as profiles_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(doctors_router)
app.include_router(patients_router)
app.include_router(appointments_router)
app.include_router(medical_records_router)
app.include_router(prescriptions_router)
app.include_router(lab_reports_router)
app.include_router(profiles_router)

@app.get("/")
def root():
    return {"message": "Healthcare Portal API is running"}