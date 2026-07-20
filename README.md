# AI Post Generator

A robust, modular, AI-powered web application built with the Flask framework that enables users to create, preview, publish, and schedule professional LinkedIn posts. The application integrates OpenAI for AI-generated text and images, LinkedIn OAuth 2.0 for account integration, Redis Queue for asynchronous background processing, and APScheduler for automatic post publishing.

---

## 🚀 Key Features

* **Secure User Authentication:**User registration, login, logout, JWT authentication, and email verification using OTP.
* **Password Recovery:** Secure password reset using email OTP verification.
* **AI Content Generation:** Generate professional LinkedIn posts using the OpenAI API.
* **AI Image Generation:** Create AI-generated images to accompany LinkedIn posts.
* **Custom Image Upload:** Upload personal images for LinkedIn posts.
* **LinkedIn Integration:** Connect and disconnect LinkedIn accounts securely using OAuth 2.0.
* **Direct LinkedIn Publishing:** Publish generated posts directly to LinkedIn.
* **Post Scheduling:** Schedule LinkedIn posts for automatic publishing at a future date and time.
* **Background Task Processing:** Email delivery handled asynchronously using Redis Queue (RQ).
* **Responsive User Interface:** Built with Bootstrap, HTML, CSS, and JavaScript for a clean and responsive experience.

---

## 🛠️ Tech Stack & Dependencies

### Backend

* Python
* Flask
* SQLAlchemy
* MySQL
* Flask-JWT-Extended
* Flask-Mail
* Redis
* Redis Queue (RQ)
* APScheduler
* OpenAI API
* OAuth 2.0
* Python-dotenv

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

---

## 📦 Major Python Packages

| Package | Purpose |
|----------|---------|
| Flask | Web framework |
| Flask-SQLAlchemy | Database ORM |
| Flask-JWT-Extended | JWT Authentication |
| Flask-Mail | Email services |
| Flask-CORS | Cross-Origin Resource Sharing |
| OpenAI | AI text and image generation |
| Requests | LinkedIn API communication |
| Redis | Background task storage |
| RQ | Background task execution |
| APScheduler | Scheduled publishing |
| bcrypt | Password hashing |
| PyMySQL | MySQL connector |
| python-dotenv | Environment variable management |

---

## 📁 Project Structure

```text
AI-Post-Generator/
│
├── app.py
├── config.py
├── database.py
├── extensions.py
├── redis_queue.py
├── worker.py
├── requirements.txt
├── .env
├── .venv/
│
├── middlewares/
│   └── auth.py
│
├── models/
│   ├── user.py
│   ├── otp.py
│   ├── password_reset.py
│   ├── linkedin.py
│   ├── post.py
│   └── scheduled_post.py
│
├── routes/
│   ├── auth.py
│   ├── linkedin.py
│   ├── pages.py
│   ├── posts.py
│   └── user.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── verify_otp.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── auth.js
│       ├── auth_guard.js
│       └── dashboard.js
│
├── utils/
│   ├── email_service.py
│   ├── linkedin_service.py
│   ├── scheduler_service.py
│   └── security.py
│
└── workers/
    └── otp_worker.py
```

---

## 🗄️ Database Architecture

The application uses a relational database managed by SQLAlchemy.

### User

Stores:

- Username
- Email
- Password (hashed)
- Email verification status

### OTP

Stores:

- Email
- Username
- Password (encrypted)
- OTP
- Expiration time

### PasswordResetOTP

Stores:

- Email
- OTP
- Expiration time

### LinkedInProfile

Stores:

- LinkedIn User ID
- First Name
- Last Name
- Email
- Profile Picture
- Headline
- OAuth Access Token

### GeneratedPost

Stores:

- Post Topic
- AI Generated Content
- Image Path
- Image Type
- Creation Time
- User ID

### ScheduledPost

Stores:

- User ID
- Scheduled Content
- Image
- Scheduled Publishing Time

---

## 🔐 Authentication & Middleware

### login_required

Protects authenticated routes by ensuring the user has a valid JWT token before accessing protected pages.

### guest_only

Prevents authenticated users from accessing Login and Signup pages.

---

## 📄 Project Modules

### app.py

Main application entry point.

Responsibilities:

- Initialize Flask
- Register Blueprints
- Configure JWT
- Initialize SQLAlchemy
- Configure Flask-Mail
- Enable CORS
- Initialize APScheduler
- Create database tables

---

### config.py

Stores all application configuration.

Includes:

- Secret Keys
- JWT Secret
- Database URL
- OpenAI API Key
- LinkedIn OAuth Credentials
- Email Configuration

---

### database.py

Initializes SQLAlchemy.

---

### extensions.py

Initializes reusable Flask extensions.

Currently contains:

- APScheduler

---

### redis_queue.py

Creates Redis connection and initializes the OTP queue.

---

### worker.py

Starts the Redis Queue worker.

---

## 📧 Email Service

Handles:

- OTP generation
- Registration verification emails
- Password reset emails

Uses Flask-Mail.

---

## 🤖 LinkedIn Service

Responsible for:

- Uploading images
- Registering media assets
- Publishing LinkedIn posts
- LinkedIn API communication

---

## ⏰ Scheduler Service

Uses APScheduler to:

- Retrieve scheduled posts
- Verify LinkedIn connection
- Publish posts
- Delete completed scheduled posts

---

## 🔒 Security

Uses bcrypt to:

- Hash passwords
- Verify passwords

---

## ⚙️ Background Workers

### otp_worker.py

Processes asynchronous email tasks using Redis Queue.

Handles:

- Signup OTP emails
- Password reset OTP emails

---

## ⚙️ Local Setup & Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd AI-Post-Generator
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file.

```env
SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret

DATABASE_URL=mysql+pymysql://username:password@localhost:3306/ai_post_generator

OPENAI_API_KEY=your_openai_api_key

LINKEDIN_CLIENT_ID=your_client_id

LINKEDIN_CLIENT_SECRET=your_client_secret

LINKEDIN_REDIRECT_URI=http://localhost:5000/linkedin/callback

MAIL_SERVER=smtp.gmail.com

MAIL_PORT=587

MAIL_USERNAME=your_email

MAIL_PASSWORD=your_email_password

MAIL_USE_TLS=True

REDIS_URL=redis://localhost:6379
```

---

### 5. Create Database

Run:

```bash
flask shell
```

```python
from database import db

db.create_all()
```

---

### 6. Start Redis Server

```bash
redis-server
```

---

### 7. Start Redis Worker

```bash
python worker.py
```

---

### 8. Run Flask Application

```bash
flask run
```

Visit:

```
http://127.0.0.1:5000
```

---

## 🚀 Application Workflow

1. User signs up with username, email, and password.
2. OTP is sent to the registered email.
3. User verifies the OTP.
4. User logs in using JWT authentication.
5. User connects their LinkedIn account through OAuth 2.0.
6. User generates AI-powered LinkedIn content.
7. User optionally generates or uploads an image.
8. User previews the generated content.
9. User either:
   - Publishes immediately, or
   - Schedules the post for future publishing.
10. APScheduler automatically publishes scheduled posts.
11. Redis Queue processes email tasks asynchronously.

---

## 🔒 Security Features

- JWT Authentication
- Password Hashing using bcrypt
- Email OTP Verification
- Password Reset OTP
- LinkedIn OAuth 2.0 Authentication
- Environment Variable Management using `.env`