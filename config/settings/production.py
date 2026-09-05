import os

from .base import *
from .base import env_bool

DEBUG = env_bool("DEBUG", default=False)

if env_bool("USE_SQLITE", default=False):
    raise ValueError("USE_SQLITE is not allowed with production settings.")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "devdesk"),
        "USER": os.getenv("POSTGRES_USER", "devdesk"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", default=True)
