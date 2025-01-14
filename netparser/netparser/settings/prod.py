import os

from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'postgres_container',
        'PORT': 5432
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis_container", 6379)],
        },
    }
}

SCRAPYD_HOST = 'http://scrapyd_container:6800'
BROKER_URL = 'redis://redis_container:6379/1'

CSRF_TRUSTED_ORIGINS = [
    'https://netparser.work.gd',
    'http://netparser.work.gd'
]

# https
CSRF_COOKIE_SECURE = True  # cookie-файлы только по протоколу HTTPS
SESSION_COOKIE_SECURE = True  # браузеры будут передавать cookie-файлы только по протоколу HTTPS

# SECURE_SSL_REDIRECT = True  # HTTP-запросы перенаправляются на HTTPS

# http
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False

# unicorn --bind 0.0.0.0:8003 --env=DJANGO_SETTINGS_MODULE=netparser.settings.local --log-level debug --access-logfile=access.logs --error-logfile=error.logs --workers=1 netparser.wsgi"