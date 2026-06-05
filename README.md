# AfyaTrace

> Secure, consent-based health records for patients and clinicians in Kenya.

AfyaTrace gives patients ownership of their medical history while enabling doctors to access records securely — with explicit patient consent via USSD before any data is shared.

---

## The Problem

In many Kenyan healthcare settings, a patient's records are scattered across different hospitals and clinics, inaccessible to the next doctor they visit. AfyaTrace centralizes that history and puts the patient in control of who sees it.

---

## Features

**Patient Portal**
- Register and log in with a national ID number
- View full visit history: diagnoses, doctor notes, and prescriptions
- Blood type and allergy information visible at a glance

**Doctor Dashboard**
- Search for any patient by national ID number
- Consent-gated access — a USSD prompt is sent to the patient's phone before records are revealed
- Simulate Access button for demo/development (bypasses the USSD step)
- Add new visit records: chief complaint, diagnosis, notes, and multiple prescriptions
- End Session button wipes patient data from the view immediately

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.x |
| Database | SQLite (development) |
| Auth | Django's built-in auth with a custom `User` model |
| Frontend | Server-rendered Django templates + vanilla JS |
| USSD (planned) | Africa's Talking API |

---

## Project Structure

```
afyatrace/
├── afyatrace/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py        # User, Patient, Doctor, Visit, Prescription
│   ├── views.py         # Page views + JSON API endpoints
│   ├── forms.py         # Registration forms for patients and doctors
│   ├── urls.py
│   └── migrations/
├── templates/
│   └── core/
│       ├── base.html
│       ├── landing.html
│       ├── patient_login.html
│       ├── patient_register.html
│       ├── patient_dashboard.html
│       ├── doctor_login.html
│       ├── doctor_register.html
│       └── doctor_dashboard.html
├── static/
├── db.sqlite3
└── manage.py
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

## Demo Accounts

The database ships with pre-seeded accounts for quick testing.

| Role | Username | Password |
|---|---|---|
| Doctor | `dr_wanjiku` | `test1234` |
| Patient | `Annita` | `test1234` |

The sample patient's national ID is `12345678` — use this in the doctor's search field.

### Trying the Doctor Flow

1. Log in as `dr_wanjiku`
2. Enter `12345678` in the Patient Lookup field and click **Search**
3. The consent panel appears, simulating a USSD prompt being sent to the patient
4. Click **⚡ Simulate Access** to load the patient's records
5. Click **➕ Add New Visit** to add a diagnosis and prescriptions
6. Click **🔒 End Session** when done — patient data is cleared from the view

---

## Data Models

```
User          — extends Django's AbstractUser; adds a role field (patient / doctor)
Patient       — linked to User; stores id_number, DOB, blood type, allergies
Doctor        — linked to User; stores license number, specialization, hospital
Visit         — links a Patient to a Doctor; stores complaint, diagnosis, notes
Prescription  — linked to a Visit; stores medication, dosage, frequency, duration
```

---

## Roadmap

- [ ] Integrate Africa's Talking USSD for real patient consent
- [ ] Switch to PostgreSQL for production
- [ ] Add SMS notifications for new visit records
- [ ] Patient ability to revoke access or view access logs
- [ ] PDF export of visit history
- [ ] Admin panel for facility management
- [ ] Deploy to a cloud host (e.g. Railway, Render, or a Kenyan VPS)

---
