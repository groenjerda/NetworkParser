from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'parser'

urlpatterns = [
    path('', cache_page(settings.CACHE_TIMEOUT, key_prefix='main_page')(views.parser), name='parser'),
]
