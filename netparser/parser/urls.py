from django.urls import path

from . import views

app_name = 'parser'

urlpatterns = [
    path('', views.parser, name='parser'),
]