🏢 Society Management System

📌 Project Overview

The Society Management System is a role-based web application developed using Django.
It allows an Admin to manage societies, flats, owners, tenants, and maintenance bills.

The system implements authentication, role-based access control, and basic CRUD operations.

🛠️ Technology Stack

Backend: Python 3, Django

Database: SQLite

Frontend: Django Templates (HTML/CSS)

Authentication: Django Built-in Authentication

Email Backend: Console Email Backend

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/GauravThorve/society-management-system.git
cd society-management-system

2️⃣ Create Virtual Environment
python -m venv env


Activate environment:

Windows

env\Scripts\activate


Mac/Linux

source env/bin/activate

3️⃣ Install Dependencies
pip install django

4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create Superuser (Admin)
python manage.py createsuperuser


Enter email, username, and password.

6️⃣ Run the Server
python manage.py runserver


Open in browser:

http://127.0.0.1:8000/

👥 User Roles

The system supports three user roles:

Admin

Owner

Tenant

Each user has:

role field

is_active field

Only active users are allowed to log in.

🔐 Authentication & Redirection

Single login page for all users.

After login:

Admin → Admin Dashboard

Owner → Owner Dashboard

Tenant → Tenant Dashboard

Unauthorized users cannot access other dashboards.

🛠️ Admin Functionalities

Admin can:

Create Owner accounts

Assign OWNER role

Activate / Deactivate Owner accounts

Create Society (Name, Address)

Create Flats (Flat Number, Assigned Owner)

Create Maintenance Bills

Send login credentials via console email

Owners cannot self-register.

🏠 Owner Functionalities

After login, Owner can:

View assigned flat details

View society details

View maintenance bills

View payment status (PAID / UNPAID)

🏢 Tenant Functionalities

After login, Tenant can:

View assigned flat details

View related society information

💰 Maintenance Bills

Admin can create bills with:

Flat

Month

Amount

Status (PAID / UNPAID)

Owners can view maintenance bill details and payment status.

(No payment gateway integration is included.)

🔒 Access Control

Admin cannot access Owner/Tenant dashboards

Owner cannot access Admin dashboard

Unauthorized users are restricted using custom decorators

🗂️ Models Overview

Custom User Model (with role field)

Society

Flat

Maintenance Bill

Tenant Profile (if implemented)

Relationships:

One Society → Multiple Flats

One Flat → One Owner

One Flat → Multiple Bills

----Features Implemented----

Django Admin Panel

Console Email Backend

Role-based access decorators

Basic validation handling

Email sending is simulated using Django console backend

📦 Submission

GitHub Repository:
https://github.com/GauravThorve/society-management-system

🎯 Evaluation Criteria Covered

✔ Django project structure
✔ Models and relationships
✔ Authentication & role-based access
✔ Code organization
✔ Basic UI clarity
