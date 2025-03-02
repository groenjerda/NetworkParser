import requests

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import ProgrammingError
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache


from scrapyd_api import ScrapydAPI

from .forms import ParserForm
from tasks.models import Task
from tasks.monitor import monitor_task


PROJECT_NAME = 'ip_networks'
SPIDER = 'networks'
PENDING = 'pending'


def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated:
            return (
                bool(user.groups.filter(name__in=group_names))
                or user.is_superuser
            )
        return False
    return user_passes_test(in_groups, login_url=reverse_lazy('parser:parser'))


class Parser(LoginRequiredMixin, View):
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        try:
            tasks = Task.objects.filter(user=request.user)
            len(tasks)
        except ProgrammingError as er:
            print(type(er))
            # Уведомить пользователя о том, что нет соединения с базой данных
            # Или о том, что модели не созданы
            tasks = []
        return render(
            request, 'parser/parser.html',
            context={
                'form': ParserForm,
                'tasks': tasks
            }
        )

    @method_decorator(group_required('users'))
    def post(self, request, *args, **kwargs):
        input_data = request.POST.get('link')
        scrapyd = ScrapydAPI(settings.SCRAPYD_HOST)
        jobid = scrapyd.schedule(PROJECT_NAME, SPIDER, link=input_data)
        # http://127.0.0.1:6800/logs/ip_networks/networks/{{task.description}}.log
        task = Task(
            name=input_data, description=jobid,
            user=request.user, status=PENDING
        )
        task.save()
        task_as_dict = model_to_dict(task)
        task_as_dict['created'] = task.created.strftime('%d.%m.%Y %H:%M')
        task_as_dict['absolute_url'] = task.get_absolute_url()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'task_from_user_{self.request.user.id}',
            {
                'type': 'send_new_task',
                'task': task_as_dict
            }
        )

        monitor_task.delay(task.id, self.request.user.id)
        return JsonResponse(task_as_dict)


class GetLog(LoginRequiredMixin, View):
    @method_decorator(group_required('users'))
    def get(self, request, *args, **kwargs):
        # http://127.0.0.1:6800/logs/ip_networks/networks/41761e44d7d611efa5820242ac140003.log
        url = '/'.join((
            settings.SCRAPYD_HOST, 'logs',
            settings.BOT_NAME, settings.SPIDER_NAME,
            f'{kwargs.get('job_id')}.log'
        ))
        response = requests.get(url)
        if response.status_code == 200:
            log_content = response.text
            if not log_content:
                log_content = 'Лог файл пустой'
        else:
            log_content = 'Лог файл не найден. Возможно, уже удален.'

        try:
            tasks = Task.objects.filter(user=request.user)
            len(tasks)
        except ProgrammingError as er:
            print(type(er))
            # Уведомить пользователя о том, что нет соединения с базой данных
            # Или о том, что модели не созданы
            tasks = []
        return render(
            request, 'parser/logs.html',
            context={
                'log_content': log_content,
                'tasks': tasks
            }
        )
