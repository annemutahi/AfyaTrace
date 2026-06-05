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

### Installation

```bash
# 1. Unzip and enter the project
unzip afyatrace_mvp.zip
cd afyatrace

# 2. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install Django
pip install django

# 4. Apply migrations
python manage.py migrate

# 5. Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Demo Accounts

The database ships with pre-seeded accounts for quick testing.

| Role | Username | Password |
|---|---|---|
| Doctor | `dr_wanjiku` | `test1234` |
| Patient | `juma_k` | `test1234` |

The sample patient's national ID is `12345678` — use this in the doctor's search field.

### Trying the Doctor Flow

1. Log in as `dr_wanjiku`
2. Enter `12345678` in the Patient Lookup field and click **Search**
3. The consent panel appears, simulating a USSD prompt being sent to the patient
4. Click **⚡ Simulate Access** to load the patient's records
5. Click **➕ Add New Visit** to add a diagnosis and prescriptions
6. Click **🔒 End Session** when done — patient data is cleared from the view

---

## API Endpoints

These are internal JSON endpoints used by the doctor dashboard.

| Method | URL | Description |
|---|---|---|
| `GET` | `/api/search-patient/?id_number=` | Check if a patient exists by ID |
| `GET` | `/api/simulate-access/?patient_id=` | Fetch full patient record (post-consent) |
| `POST` | `/api/add-visit/` | Save a new visit with prescriptions |

All endpoints require an authenticated doctor session and include CSRF protection.

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

## Security Notes

This is an MVP for development and demonstration purposes. Before going to production:

- Replace `SECRET_KEY` in `settings.py` with a strong, randomly generated value stored in an environment variable
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` properly
- Switch to PostgreSQL or another production-grade database
- Enforce HTTPS
- Add rate limiting to the patient search and access endpoints
- Implement a real USSD consent flow — the simulate button must not exist in production

---

## License

MIT — free to use, modify, and build on.
