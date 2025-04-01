# Django Blog Project

This is a simple blog project built with Django.

## Features
- User authentication (Login/Register)
- Create, edit, and delete blog posts
- Upload images for blog posts
- Responsive design using Bootstrap
- CSRF protection enabled

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Diluxshan06/django-blog-postgres.git
cd django-blog-postgres
```

### 2. Create and Activate a Virtual Environment
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create a Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 6. Run the Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
Open your browser and go to:
- **Home Page:** `http://127.0.0.1:8000/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`

## Usage
- Register or login to create and manage blog posts.
- Admins can manage users and posts from the Django admin panel.

 `dinuluxshan110@gmail.com`

