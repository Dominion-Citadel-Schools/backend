from .base import *
from decouple import config
import os



DEBUG = False

host = os.environ.get("HTTP_HOST", "")

if "staging" in host:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.staging")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

STATIC_URL = "/static/"
STATIC_ROOT = "/home/domiloph/staging.dominioncitadelschools.com/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/domiloph/staging.dominioncitadelschools.com/media"

APP_ENV = "prod"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True

APPEND_SLASH = False

DATABASES = {
    'default': {
           'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME_SG'),
            'USER': config('DB_USER_SG'),
            'PASSWORD': config('DB_PASSWORD_SG'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/domiloph/production_cache',
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "staging.dominioncitadelschools.com"

EMAIL_PORT = 465

EMAIL_USE_SSL = True

EMAIL_TIMEOUT = 20

EMAIL_HOST_USER = "noreply@staging.dominioncitadelschools.com"

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = "Dominion Citadel Schools <noreply@staging.dominioncitadelschools.com>"