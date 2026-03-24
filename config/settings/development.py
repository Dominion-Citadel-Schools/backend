from .base import *
from decouple import config


DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

APP_ENV = "dev"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

DATABASES = {
    'default': {
           'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME_DV'),
            'USER': config('DB_USER_DV'),
            'PASSWORD': config('DB_PASSWORD_DV'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
    }
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-dominion-schools-v1-cache"
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_TIMEOUT = 20

EMAIL_HOST_USER = "ohibor@gmail.com"

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD_DEV')

DEFAULT_FROM_EMAIL = "Dominion Citadel Schools <ohibor@gmail.com>"