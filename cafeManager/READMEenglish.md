# Cafe Manager – README

A simple but fully functional café management and ordering system built with **Django** and **SQLite3** (easily extendable to PostgreSQL or MySQL).  
The platform supports **user registration**, **login with Remember Me**, **soft account deletion**, **order management**, **item management**, and a full **admin dashboard** with permission control.

---

# 📌 Features Overview

## ✔ Normal User Features

Normal authenticated users can:

- **Overview Dashboard** – view basic account and order information.
- **My Orders** – view *only their own orders*.
- **Profile** – update personal information (full name, email, password, etc.).
- **Place Orders** – order items available in the system.
- **Soft Delete Account** – the user can delete their account from profile settings (account becomes inactive).
- **Login with Remember Me**  
  - When "Remember Me" is checked, a session cookie is created that lasts **30 days**.

---

## ✔ Admin User Features

Admins have full access to the system and dashboard:

- **Admin Dashboard**
- **All Orders** – view, filter, and manage all orders.
- **Categories** – add, edit, delete categories.
- **Tags** – create, assign, and manage tags for items.
- **Add Item** – upload items with images, categories, tags, and prices.
- **Edit Items** – update or delete existing items.
- **Manage Users**
  - Promote any user to **Admin**
  - Mark users as **Staff**
  - Revoke admin/staff permissions
- **View All User Orders**

### 🔒 Admin-Only Route Enforcement
If a **normal user** tries to access admin-only routes like:

```commandline
http://127.0.0.1:8000/dashboard/admin/orders/
```
They receive:
``
403 Forbidden
``

Admins can access all admin routes normally.

---

## ✔ Error Handling

### **404 – Page Not Found**
If a user visits an invalid or missing item page, such as:
```commandline
http://127.0.0.1:8000/item/6/
```

A custom  displays: ``
**404 error page**
``

- Clean UI
- Friendly message
- Navigation back to home

### **403 – Forbidden**
Shown when a normal user attempts to access admin-only pages.

> ✔ Both custom error pages work even when `DEBUG = True`.

---

# 🛠 Technology Stack

- **Backend:** Django (Python)
- **Database:** SQLite3 (default)
- **Templating:** Django Template Engine
- **Authentication:** Django Auth + Remember Me (30-day cookie)
- **Permissions:** Django decorators + custom permission checks

You can switch the database engine to **PostgreSQL** or **MySQL** easily by editing `settings.py`.

---

# 🔧 Installation & Setup

## 1️⃣ Clone the repository
```commandline
git clone https://github.com/Wambong/testtask.git
```
2️⃣ Create a virtual environment
```commandline
cd testtask/cafeManager
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```
3️⃣ Install dependencies
```commandline
pip install -r requirements.txt
```
4️⃣ Apply migrations

```commandline
python manage.py migrate
```
5️⃣ Create a superuser (admin account)
```commandline
python manage.py createsuperuser
```
6️⃣ Run the development server
```commandline
python manage.py runserver
```

📂 Project Structure (Important Folders)

```commandline
accounts/               → User authentication, profiles, permissions
orders/                 → Items, categories, tags, and orders logic
templates/              → HTML templates
static/                 → Images, CSS, JS assets
cafeManager/readme     → Images used only in the README.md

```
# 💾 Database Support
## Default database: SQLite3
## To switch to PostgreSQL:

```commandline
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cafe_db',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```

# email
```commandline
admin@gmail.com
```
# password
```commandline
Addmminna
```
```commandline
http://127.0.0.1:8000/dashboard/
```
![img_7.png](cafeManager/readme/img_7.png)

```commandline
http://127.0.0.1:8000/dashboard/admin/orders/
```
![img_8.png](cafeManager/readme/img_8.png)

```commandline
http://127.0.0.1:8000/accounts/admin/users/
```
![img_9.png](cafeManager/readme/img_9.png)
## normal user 
```commandline
wa@gmail.com
```
```commandline
sfdgjdfg45
```

![img.png](cafeManager/readme/img.png)

![img_1.png](cafeManager/readme/img_1.png)

![img_2.png](cafeManager/readme/img_2.png)

![img_3.png](cafeManager/readme/img_3.png)

![img_4.png](cafeManager/readme/img_4.png)

```commandline
http://127.0.0.1:8000/dashboard/admin/orders/
```
![img_5.png](cafeManager/readme/img_5.png)

```commandline
http://127.0.0.1:8000/item/6/
```
![img_6.png](cafeManager/readme/img_6.png)