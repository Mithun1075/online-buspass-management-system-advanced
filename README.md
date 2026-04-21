# 🚌 Online Bus Pass Management System (Advanced)

## 📌 Overview
An advanced full-stack web application built using Django to automate the complete bus pass lifecycle, including application, verification, approval, payment, and renewal.  
The system ensures a secure, efficient, and paperless workflow.

---

## 🚀 Key Features

- 🔐 OTP-based user registration with email verification  
- 👥 Role-based access control (User & Verification Officer)  
- 🔄 Workflow management:  
  - Pending → Approved / Rejected → Completed  
- 💳 Email-triggered payment link after approval  
- 🔁 Smart renewal system with expiry validation  
- 🎫 Digital E-Pass generation with unique ID and validity  
- 📧 Automated email notifications:
  - Approval / Rejection  
  - Payment confirmation  
  - Renewal alerts  

---

## 🛠️ Tech Stack

- **Backend:** Python, Django  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** MySQL  
- **Authentication:** Django Sessions  
- **Email Integration:** SMTP  

---

## 🧠 Core Concepts Used

- Django ORM  
- Authentication & Authorization  
- Session Management  
- MVC Architecture  
- Email Automation  

---

## ⚙️ Installation & Setup

```bash
git clone https://github.com/your-username/online-buspass-management-system-advanced.git
cd online-buspass-management-system-advanced
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

---

## 🔥 Quick Note

- `makemigrations` → Create database schema changes  
- `migrate` → Apply changes to database  
- `createsuperuser` → Create admin login (for Django admin panel)  
- `runserver` → Start development server  
