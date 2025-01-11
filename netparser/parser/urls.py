from django.urls import path

from . import views

app_name = 'parser'

urlpatterns = [
    path('', views.Parser.as_view(), name='parser')
]
