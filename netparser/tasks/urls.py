from django.urls import path

from . import views

app_name = 'tasks'


urlpatterns = [
    # path('', cache_page(settings.CACHE_TIMEOUT, key_prefix='main_page')(views.parser), name='parser'),  # noqa
    path('', views.tasks, name='tasks'),
    path('remove/', views.remove_tasks, name='remove'),
    path('<int:taskid>/status/', views.TaskStatus.as_view(), name='status'),
    path('<int:taskid>/', views.TaskDetail.as_view(), name='detail')
]
