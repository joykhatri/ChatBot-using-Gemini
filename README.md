# Chat-Bot-using-Gemini
Integrating Gemini models in the django &amp; django rest framework project. Develop own chatbot using Gemini Models.

## TechStack
- Backend:- Django, DjagoRestFramework
- Frontend (GUI):- tkinter

## get GEMINI API KEY

- go to https://aistudio.google.com/
- Login with google account
- click Get API key
- click Create API key
- create new project/import project (if you not get any default project)
- after creating project you get your API KEY

## 🚀 Setup Instructions

### 1️⃣ Create Virtual Environment
```bash
python -m venv .venv
```

### 2️⃣ Activate Virtual Environment
```bash
.venv\Scripts\activate
```

### Linux/macOS:
```bash
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install django djangorestframework mysqlclient
pip install google-generativeai
pip install djangorestframework-simplejwt     # JWT Authentication
```

### 4️⃣ Start Django Project & App
```bash
django-admin startproject gemini_chatbot_project .
django-admin startapp gemini_app
```

### 5️⃣ Add Apps to INSTALLED_APPS (project/settings.py)
```bash
INSTALLED_APPS = [
    ...
    'gemini_app',
    'rest_framework',
]
```

### 6️⃣ Configure MySQL Database (settings.py)
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',   # Or your DB host
        'PORT': '3306',
    }
}
```

### 7️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8️⃣ Run Server
### Development server:
```bash
python manage.py runserver
```

- start development server and with that open new terminal and run
- ```bash
  python gemini.py
  ```
- for tkinter GUI (for Chat)

## 🔑 API Endpoints

| Method | Endpoint                                            | Description                              |
| ------ | --------------------------------------------------- | ---------------------------------------- |
| POST   | `/api/register/`                                    | User Registration                        |
| POST   | `/api/login/`                                       | User Login                               |
| POST   | `/chat/`                                            | For Chat with Gemini                     |

### Register
```bash
{
    "name": "demo",
    "email": "demo@gmail.com",
    "password": "demo@123",
}
```

### Login
```bash
{
    "email": "demo@gmail.com",
    "password": "demo@123"
}
```

### Chat
```bash
{
    "message": "why sky is blue?"
}
```
