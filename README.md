# CampusCore - Student Management System 🎓

[![GitHub stars](https://img.shields.io/github/stars/PankajjPatel/Campus-Core?style=for-the-badge&color=blue)](https://github.com/PankajjPatel/Campus-Core/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/PankajjPatel/Campus-Core?style=for-the-badge&color=teal)](https://github.com/PankajjPatel/Campus-Core/network/members)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0%2B-green?style=for-the-badge&logo=django)](https://djangoproject.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=for-the-badge&logo=mysql)](https://mysql.com)

> **Slogan:** The Core of Campus Management 🏫  
> **Tagline:** Empowering educational institutions with seamless administration, unified workflows, and modern analytics in a single secure workspace.

CampusCore is a complete, production-ready Student Management System built on Python and Django using a MySQL database and custom Tailwind CSS styling. It provides robust workflows for Super Administrators and Faculty Members, alongside a public Student Portal to search timetables, announcements, and performance report cards.

--- 

## 🛠️ Tech Stack & Key Libraries
- **Backend:** Python 3.10+ & Django 6.0+
- **Database:** MySQL Server 8.0 (configured with standard Django ORM & pure Python `pymysql` client)
- **UI / UX Styling:** Tailwind CSS v3 via CDN (supporting global light & class-based dark mode) with Lucide Icons CDN.
- **Reporting Engine:**
  - `openpyxl` (Exports student/teacher listings dynamically to Excel sheets)
  - `reportlab` (Generates academic semester report cards as PDFs)

---hi

## 🔑 User Authentication Credentials

### 1. Super Administrator Account
- **Username:** `_pankaj_09`
- **Password:** `Pankaj@123`
- *Note:* Registration of admin accounts is restricted (there is exactly one admin). Public signup is disabled for security.

### 2. Faculty / Teacher Accounts
- *Note:* Teacher profiles are created exclusively by the Administrator. Below are the pre-configured accounts created during database seeding:
- **Teacher 1:** Username: `amit_teacher` | Password: `Teacher@123`
- **Teacher 2:** Username: `priya_teacher` | Password: `Teacher@123`

### 3. Student Records
- Students do not log in. They use their unique **Roll Number** on the public portal lookup box to securely inspect their grades, daily attendance, notices, and timetables.
- **Sample Students:** `CSE001` (Rahul Kumar), `CSE002` (Sneha Patel), `MTH001` (Aakash Gupta).

---

## 🚀 Step-by-Step Local Setup Guide

Follow these steps to run the CampusCore server locally on your machine:

### 1. Database Setup in MySQL
Ensure your local MySQL service is running. Run the following command in your MySQL console to initialize the schema:
```sql
CREATE DATABASE CampusCore;
```

### 2. Configure Environment/Settings
The database credentials have been pre-configured in [settings.py](file:///c:/Users/panka/CampusCore/CampusCore/settings.py) to match your environment:
- **Database Name:** `CampusCore`
- **Username:** `root`
- **Password:** `Root@123`
- **Host / Port:** `localhost` / `3306`

### 3. Apply Migrations
Open your terminal inside the `c:\Users\panka\CampusCore` directory and run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Academic Demo Data
Run our custom seeding script to populate the database tables with the default Admin user, mock classes, schedules, and student records:
```bash
python manage.py seed_data
```

### 5. Launch the Local Server
Start the Django development server:
```bash
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/`.


---

## 📂 Project Architecture Layout
- **[CampusCore/settings.py](file:///c:/Users/panka/CampusCore/CampusCore/settings.py):** Main project configuration parameters (database credentials, static files, login routes).
- **[core/models.py](file:///c:/Users/panka/CampusCore/core/models.py):** Relational database models (Course, Subject, Teacher, Student, Attendance, Result, Fee, Notice, Timetable).
- **[core/forms.py](file:///c:/Users/panka/CampusCore/core/forms.py):** Form validation logic and Tailwind widget mixins.
- **[core/views.py](file:///c:/Users/panka/CampusCore/core/views.py):** Class-Based Views (CBVs) managing dashboards, CRUD processes, bulk attendance/marks operations, and Excel/PDF reporting streams.
- **[core/urls.py](file:///c:/Users/panka/CampusCore/core/urls.py):** Routing definitions.
- **[templates/base.html](file:///c:/Users/panka/CampusCore/templates/base.html):** Layout wrapper containing the navigation sidebar, alerts panel, and responsive Light/Dark theme toggler (remembered via `localStorage`).
