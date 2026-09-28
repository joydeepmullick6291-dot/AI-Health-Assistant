from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_doctor():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "doctor1@example.com").first()
        if existing:
            print("Doctor already exists")
            return

        doctor = User(
            name="Dr. Meera Sen",
            email="doctor1@example.com",
            password=pwd_context.hash("doctor123"),
            role="doctor"
        )
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        print("Doctor user created")
    finally:
        db.close()

if __name__ == "__main__":
    create_doctor()