from .base import *
from decouple import config



DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")

STATIC_URL = "/static/"
STATIC_ROOT = "/home/domiloph/api.dominioncitadelschools.com/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/domiloph/api.dominioncitadelschools.com/media"

APP_ENV = "prod"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True

APPEND_SLASH = False

DATABASES = {
    'default': {
           'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME_PROD'),
            'USER': config('DB_USER_PROD'),
            'PASSWORD': config('DB_PASSWORD_PROD'),
            'HOST': config('DB_HOST_PROD', default='localhost'),
            'PORT': config('DB_PORT_PROD'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/domiloph/production_cache',
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "api.dominioncitadelschools.com"

EMAIL_PORT = 465

EMAIL_USE_SSL = True

EMAIL_TIMEOUT = 20

EMAIL_HOST_USER = "noreply@api.dominioncitadelschools.com"

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = "Dominion Citadel Schools <noreply@api.dominioncitadelschools.com>"