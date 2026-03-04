from .base import *

DEBUG = False

ALLOWED_HOSTS = ["yourdomain.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "chronologs",
        "USER": "postgres",
        "PASSWORD": "securepassword",
        "HOST": "db",
        "PORT": "5432",
    }
}