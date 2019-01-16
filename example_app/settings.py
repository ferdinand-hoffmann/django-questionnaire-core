# -*- coding: utf-8 -*-
"""
Minimal settings file to develop questionnaire_core.
Use `settings_local.py` to override any settings.
"""
import os


APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True

SECRET_KEY = "yRMdC-vQ4c8c*Biil(&&aEjG&cDBff=DIWp(wYRLWovM$vVC/=@CZoRO6EGX`#s"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'ordered_model',
    'questionnaire_core',
)

ROOT_URLCONF = 'example_app.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'questionnaire_core',
    },
}

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(APP_DIR, 'example_app/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(APP_DIR, 'media')
MEDIA_URL = '/media/'

try:
    from .settings_local import *  # NOQA
except ImportError:
    pass
