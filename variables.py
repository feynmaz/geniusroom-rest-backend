import os


# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG')


# Email
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# Database
POSTGRES_NAME = os.environ.get('POSTGRES_NAME')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_USER_PASSWORD = os.environ.get('POSTGRES_USER_PASSWORD')


# Client
CLIENT_URL = os.environ.get('CLIENT_URL')