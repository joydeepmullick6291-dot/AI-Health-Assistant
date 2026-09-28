# 🩺 AI Health Assistant

> An AI-powered healthcare assistant designed to simplify healthcare management through a centralized digital platform.

## 📌 Overview

**AI Health Assistant** is a full-stack healthcare management project that provides a single platform for patients and doctors to manage important healthcare-related activities.

The system combines patient management, appointments, medical records, prescriptions, laboratory reports, vital tracking, and symptom guidance into one application.

## ✨ Features

### 👤 Patient Management

* Patient registration and authentication
* Personal profile management
* Access to medical records
* Health information tracking

### 🩺 Doctor Management

* Doctor profiles
* Patient-related information
* Appointment management
* Prescription handling

### 📅 Appointment Management

* Schedule and manage appointments
* View appointment details
* Patient-doctor interaction through appointment records

### 💊 Prescriptions

* Create and manage prescriptions
* View prescribed medicines and related information

### 🧪 Laboratory Reports

* Store and manage laboratory reports
* Track lab results associated with patients

### ❤️ Health Tracking

* Record and monitor vital information
* Maintain health-related records over time

### 🤖 Symptom Guidance

* Symptom-based healthcare guidance
* Helps users understand possible health concerns and decide when professional medical attention may be appropriate

> **Note:** This project is intended for educational and demonstration purposes and should not be used as a substitute for professional medical advice.

## 🛠️ Tech Stack

**Frontend**

* HTML5
* CSS3
* JavaScript

**Backend**

* Python
* FastAPI

**Database**

* MySQL
* PyMySQL

**Authentication & Security**

* JWT-based authentication
* Password hashing
* Environment-based configuration

## 📂 Project Structure

```text
AI-Health-Assistant/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── utils/
│   ├── requirements.txt
│   └── seed_doctor.py
│
├── database/
│   └── schema.sql
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── pages/
│   ├── partials/
│   └── assests/
│
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/joydeepmullick6291-dot/AI-Health-Assistant.git
cd AI-Health-Assistant
```

### 2. Set up the backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure the database

Make sure MySQL is installed and running.

Create the required database and user, then configure your environment variables using the provided `.env.example`.

**Never commit your actual `.env` file or database credentials to GitHub.**

### 4. Start the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will start on the local development server.

### 5. Open the frontend

Open the frontend's `pages/index.html` in your browser or serve the frontend through a local web server.

## 🔐 Environment Variables

Create a `.env` file locally based on `.env.example`.

Example:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/healthcare_portal
SECRET_KEY=your-secret-key
```

**Do not upload `.env` to GitHub.**

## 🎯 Project Goals

The project was developed to demonstrate how a modern healthcare management system can be built using a **Python backend, REST APIs, database management, authentication, and an interactive web frontend**.

It also provides a foundation for adding more advanced AI-powered healthcare features in the future.

## 🔮 Future Improvements

* AI-powered conversational health assistant
* More advanced symptom analysis
* Health insights and personalized recommendations
* Doctor search and filtering
* Notifications and reminders
* Improved dashboard analytics
* Cloud deployment
* Mobile application

## 👨‍💻 Author

**Joydeep Mullick**

Built as a full-stack healthcare technology project combining web development, backend APIs, database management, and AI-oriented healthcare functionality.

---

⭐ If you find this project interesting, feel free to explore the code and give the repository a star!
