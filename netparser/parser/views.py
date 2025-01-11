from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
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
        tasks = Task.objects.filter(user=request.user)
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
            'tasks_status_updates',
            {
                'type': 'send_new_task',
                'task': task_as_dict
            }
        )

        monitor_task.delay(task.id)
        return JsonResponse(task_as_dict)
