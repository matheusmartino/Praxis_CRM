import os

from .base import *  # noqa: F401,F403

DEBUG = False

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()
]



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "praxiscrm"),
        "USER": os.getenv("DB_USER", "praxiscrm"),
        "PASSWORD": os.getenv("DB_PASSWORD", "Praxis@0611"),
        "HOST": os.getenv("DB_HOST", "jdbc:postgresql://praxiscrm.postgresql.dbaas.com.br:5432/praxiscrm"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
