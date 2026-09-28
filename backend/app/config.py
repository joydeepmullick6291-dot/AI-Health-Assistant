import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://health_user:your_password@localhost:3306/healthcare_portal"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "your-secret-key-here"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
