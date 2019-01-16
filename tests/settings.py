# -*- coding: utf-8 -*-
"""
Minimal settings file for automated tests.
Use `settings_local.py` to override any settings.
"""
import os


APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True

SECRET_KEY = "R(%y1oBDBjkPvYvH<d^35Iga${G'Fxuwt{:$?*&QG'Sk[+aL;ojL'xadx+S8>@@"

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = (
    'ordered_model',
    'questionnaire_core',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'questionnaire_core',
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(APP_DIR, 'tests/templates/')
        ],
        'APP_DIRS': True,
    },
]

MIDDLEWARE = (
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
}

try:
    from .settings_local import *  # NOQA
except ImportError:
    pass
