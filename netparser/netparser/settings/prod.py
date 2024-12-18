from .base import *


DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database', 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://netparser.work.gd', 'http://netparser.work.gd']

# https
CSRF_COOKIE_SECURE = True  # cookie-файлы только по протоколу HTTPS
SESSION_COOKIE_SECURE = True  # браузеры будут передавать cookie-файлы только по протоколу HTTPS

# SECURE_SSL_REDIRECT = True  # HTTP-запросы перенаправляются на HTTPS

# http
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False
