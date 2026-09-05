import os

from .base import *
from .base import BASE_DIR, env_bool

DEBUG = env_bool("DEBUG", default=True)

if env_bool("USE_SQLITE", default=False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "devdesk"),
            "USER": os.getenv("POSTGRES_USER", "devdesk"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "devdesk"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
