from django.urls import path

from . import views

app_name = 'parser'

urlpatterns = [
    path('', views.Parser.as_view(), name='parser'),
    path('log/<str:job_id>/', views.GetLog.as_view(), name='get_log')
]
