# Career Compass 🎓

> **Career Compass** is a Django-powered Web Application designed to analyze student academic performance (JSS1 – JSS3) and recommend personalized career fields and higher-education disciplines.

---

## 🌟 Key Features

- **Access Code Student Portal**: Fast, secure dashboard access for students using unique 7-digit access codes.
- **Academic Analytics & Performance Charts**: Dynamic visual score tracking across grade levels and session terms powered by Chart.js.
- **Career Path Prediction Algorithm**: Intelligently aggregates top-performing subject fields to recommend matching career disciplines.
- **Interactive AI Career Assistant**: Built-in interactive guidance chat interface.
- **Production & Vercel Ready**: Full WSGI support, WhiteNoise static file compression, and standard environment variable management.

---

## 🔑 Default Credentials

- **Admin Portal (`/admin/`)**:
  - **Username**: `admin`
  - **Password**: `admin123`
- **Student Portal Access Code**: `1234567` (or generate custom codes via Admin Dashboard)

---


## 🚀 Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Pradeepk0606/career-counseling.git
cd career-counseling
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Admin Superuser

```bash
python manage.py createsuperuser
```

### 7. Populate Sample Student Data (Optional)

```bash
python manage.py populate_db 5
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser. Access the Admin Panel at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

---

## 🧪 Running Unit Tests

Run the complete Django test suite:

```bash
python manage.py test
```

---

## ☁️ Deploying to Vercel

This repository includes a native `vercel.json` configuration for seamless deployment:

1. Import the repository into your [Vercel Dashboard](https://vercel.com).
2. Set Environment Variables in Vercel project settings (optional):
   - `SECRET_KEY`: Production secret key.
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.vercel.app`
3. Click **Deploy**. Vercel will automatically build the WSGI application and serve static assets via WhiteNoise.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for details.
