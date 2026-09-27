# Nabd — clinic appointments for Riyadh

Nabd (نبض, "pulse") lets patients find a clinic in Riyadh, book an appointment, pay online and
upload their medical reports before the visit. Clinics see their day's bookings in one place.

## Features

- Patient sign-up and login
- Book, view and cancel appointments
- Online payment with Moyasar (mada, Visa, Apple Pay)
- Upload medical reports (PDF or image) ahead of a visit
- Product analytics with Mixpanel
- Admin view of patients and bookings

## Stack

Flask, Flask-SQLAlchemy, Flask-Login, PostgreSQL, Amazon S3, Moyasar, Mixpanel.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then fill in your own values
flask --app wsgi run
```

## Project layout

```
app/
  __init__.py          app factory
  models.py            Patient, Appointment
  auth/                sign-up and login
  appointments/        booking, payment, report upload
  admin/               admin views
  services/            Moyasar, Mixpanel and S3 clients
  templates/
config.py
wsgi.py
```
