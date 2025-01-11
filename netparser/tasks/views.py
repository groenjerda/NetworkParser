import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .models import Task
from parser.models import AsInfo
from parser.views import group_required

PROJECT_NAME = 'ip_networks'


@login_required
@never_cache
@group_required('users')
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'parser/tasks.html', context={'tasks': tasks})


@login_required
@require_POST
@group_required('users')
def remove_tasks(request):
    ids = [int(item) for item in request.POST.getlist('ids')]
    deleted_count, _ = Task.objects.filter(
        id__in=ids, user=request.user
    ).delete()
    return JsonResponse({'deleted_count': deleted_count})


@method_decorator(group_required('users'), name='dispatch')
class TaskStatus(View, LoginRequiredMixin):
    @method_decorator(group_required('users'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['taskid'], user=request.user)
        return JsonResponse({'status': task.status})

    def post(self, request, *args, **kwargs):
        data = request.POST
        new_status = data.get('status')
        task = get_object_or_404(Task, id=kwargs['taskid'], user=request.user)
        if task.status != new_status:
            task.status = new_status
            task.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'tasks_status_updates',
                {
                    'type': 'send_status_updates',
                    'task_id': kwargs['taskid'],
                    'status': new_status
                }
            )


@method_decorator(group_required('users'), name='dispatch')
class TaskDetail(View, LoginRequiredMixin):
    @method_decorator(group_required('users'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user=request.user)
        try:
            task = tasks.get(id=kwargs['taskid'])
            as_info = AsInfo.objects.prefetch_related(
                'networks').get(jobid=task.description)
        except ObjectDoesNotExist:
            as_info = None
        return render(
            request, 'parser/task_detail.html',
            context={
                'taskid': kwargs['taskid'],
                'as_info': as_info,
                'tasks': tasks
            }
        )

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['taskid'], user=request.user)
        try:
            as_info = AsInfo.objects.prefetch_related(
                'networks').get(jobid=task.description)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=500)

        result = as_info.to_dict()
        result['networks'] = list(as_info.networks.values(
            'network', 'provider', 'country', 'ip_version'
        ))

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{as_info.name}.json"'
        )
        response.write(json.dumps(result, indent=4, default=str))
        return response
