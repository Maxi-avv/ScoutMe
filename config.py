import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///scoutme.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 104857600))  # 100MB
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')

    # Email config (optional)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')