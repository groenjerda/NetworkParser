from .base import *


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database', 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = ['*']

# https
# CSRF_COOKIE_SECURE = True  # cookie-файлы только по протоколу HTTPS
# SESSION_COOKIE_SECURE = True  # браузеры будут передавать cookie-файлы только по протоколу HTTPS
# SECURE_SSL_REDIRECT = True  # HTTP-запросы перенаправляются на HTTPS

