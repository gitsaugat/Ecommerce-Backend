from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

SECRET_KEY = os.environ.get('SECRET_KEY')

INSTALLED_APPS += []

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STRIPE_API_KEYS = {
    'pk': os.environ.get('STRIPE_PK'),
    'sk': os.environ.get('STRIPE_SK')
}
