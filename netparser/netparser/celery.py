import os

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netparser.settings.prod')
app = Celery('netparser')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.BROKER_URL
app.autodiscover_tasks()

# pip install gevent
# celery -A netparser worker --loglevel=info -P gevent
# celery -A netparser worker --loglevel=info -P eventlet
