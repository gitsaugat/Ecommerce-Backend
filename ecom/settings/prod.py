from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ['djreactecommerce.herokuapp.com']

SECRET_KEY = os.environ.get('SECRET_KEY')

CORS_ALLOWED_ORIGINS = ['https://localhost:3000']

INSTALLED_APPS += []

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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
