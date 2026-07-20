import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    print("DATABASE PATH:", SQLALCHEMY_DATABASE_URI)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    MAIL_SERVER = "smtp.gmail.com"
    
    MAIL_PORT = 587
    
    MAIL_USE_TLS = True
    
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
    
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
    
    LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")
