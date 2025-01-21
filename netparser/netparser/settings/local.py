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
        'HOST': '127.0.0.1',
        # 'HOST': 'postgres_container',
        'PORT': 5432
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [("redis_container", 6379)],
            "hosts": [("127.0.0.1", 6379)],
        },
    }
}

# SCRAPYD_HOST = 'http://scrapyd_container:6800'
SCRAPYD_HOST = 'http://127.0.0.1:6800'


# BROKER_URL = 'redis://redis_container:6379/1'
BROKER_URL = 'redis://127.0.0.1:6379/1'
