# Clinic Booking System 🏥

A full-stack clinic and doctor appointment booking web application built with **Django**, **Python**, and modern web practices. Deployed and production-ready for **Render**.

---

## 🌟 Features

- **Doctor Directory & Departments**: Browse doctors filtered by medical specialties and departments.
- **Interactive Appointment Booking**: View available time slots for doctors over the upcoming days and reserve slots with reasons for consultation.
- **Patient Dashboard**: Patients can view their booked appointments, doctor details, appointment timings, and cancel bookings if necessary.
- **Authentication**: Complete user registration and login/logout system.
- **Staff / Admin Management**: Integrated Django admin panel to manage departments, doctors, schedules, time slots, and bookings.
- **Seed Demo Data**: One-command fixture and data generator for instant development and testing (`python manage.py seed_demo`).
- **Production-Ready**: Preconfigured with `WhiteNoise` for static asset compression/serving, `Gunicorn` WSGI server, and `render.yaml` for zero-configuration Render deployments.

---

## 🛠️ Tech Stack

- **Backend**: Django 6.x, Python 3.12+
- **Database**: SQLite (Development) / PostgreSQL compatible
- **WSGI Server**: Gunicorn
- **Static Assets**: WhiteNoise
- **Deployment**: Render (`render.yaml`)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (Recommended Python 3.12)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/preethigrandhisila/clinic_booking.git
cd clinic_booking
```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Seed Demo Data (Optional)

Populate departments, doctors, and available slots for the upcoming 7 days:

```bash
python manage.py seed_demo
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Or use the environment-aware script:
# ADMIN_USERNAME=admin ADMIN_PASSWORD=yourpassword python create_superuser.py
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to:
- App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🌐 Deployment to Render

The repository includes a `render.yaml` blueprint. To deploy:

1. Push this repository to GitHub.
2. Sign in to [Render](https://render.com/).
3. Create a **New Blueprint Instance** and connect your `clinic_booking` repository.
4. Render will automatically detect `render.yaml` and configure:
   - Python 3.12 environment
   - Dependency installation
   - Static asset collection via WhiteNoise
   - Database migrations & initial setup
   - Production Gunicorn WSGI web service

---

## 📁 Project Structure

```
clinic_booking/
├── booking/                     # Core booking application
│   ├── fixtures/                # Sample data fixtures
│   ├── management/commands/     # Custom commands (seed_demo)
│   ├── migrations/              # Database migrations
│   ├── static/                  # CSS & JavaScript files
│   ├── templates/booking/       # HTML templates
│   ├── admin.py                 # Admin configuration
│   ├── forms.py                 # Booking and auth forms
│   ├── models.py                # Department, Doctor, TimeSlot, Appointment models
│   ├── urls.py                  # App URL routing
│   └── views.py                 # View controllers
├── clinic/                      # Project settings & WSGI
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── create_superuser.py          # Script for programmatic superuser creation
├── manage.py                    # Django CLI entrypoint
├── render.yaml                  # Render deployment configuration
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 📄 License

This project is licensed under the MIT License.